from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from ..db import get_db
from ..models import ActionItem, Note, Tag
from ..schemas import NoteCreate, NoteRead, NoteTagRequest, NoteUpdate, SuccessEnvelope
from ..services.extract import extract_content

router = APIRouter(prefix="/notes", tags=["notes"])


def serialize(note: Note) -> dict:
    return NoteRead.model_validate(note).model_dump()


def get_note_or_404(db: Session, note_id: int) -> Note:
    note = db.scalar(select(Note).options(selectinload(Note.tags)).where(Note.id == note_id))
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("", response_model=SuccessEnvelope)
@router.get("/", response_model=SuccessEnvelope, include_in_schema=False)
def list_notes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    tag: str | None = Query(None, min_length=1, max_length=50),
    db: Session = Depends(get_db),
) -> dict:
    query = (
        select(Note)
        .options(selectinload(Note.tags))
        .order_by(Note.created_at.desc(), Note.id.desc())
    )
    count_query = select(func.count(Note.id))
    if tag:
        normalized = tag.strip().lstrip("#").lower()
        query = query.join(Note.tags).where(Tag.name == normalized)
        count_query = count_query.join(Note.tags).where(Tag.name == normalized)
    total = db.scalar(count_query) or 0
    rows = db.scalars(query.offset((page - 1) * page_size).limit(page_size)).all()
    return {
        "ok": True,
        "data": {
            "items": [serialize(row) for row in rows],
            "total": total,
            "page": page,
            "page_size": page_size,
        },
    }


@router.get("/search", response_model=SuccessEnvelope)
@router.get("/search/", response_model=SuccessEnvelope, include_in_schema=False)
def search_notes(
    q: str = Query("", max_length=200),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort: Literal["created_desc", "title_asc"] = "created_desc",
    db: Session = Depends(get_db),
) -> dict:
    query = select(Note).options(selectinload(Note.tags))
    count_query = select(func.count(Note.id))
    term = q.strip()
    if term:
        pattern = f"%{term.lower()}%"
        predicate = or_(
            func.lower(Note.title).like(pattern),
            func.lower(Note.content).like(pattern),
        )
        query = query.where(predicate)
        count_query = count_query.where(predicate)
    if sort == "title_asc":
        query = query.order_by(func.lower(Note.title).asc(), Note.id.asc())
    else:
        query = query.order_by(Note.created_at.desc(), Note.id.desc())
    total = db.scalar(count_query) or 0
    rows = db.scalars(query.offset((page - 1) * page_size).limit(page_size)).all()
    return {
        "ok": True,
        "data": {
            "items": [serialize(row) for row in rows],
            "total": total,
            "page": page,
            "page_size": page_size,
        },
    }


@router.post("", response_model=SuccessEnvelope, status_code=201)
@router.post("/", response_model=SuccessEnvelope, status_code=201, include_in_schema=False)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> dict:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return {"ok": True, "data": serialize(note)}


@router.get("/{note_id}", response_model=SuccessEnvelope)
def get_note(note_id: int, db: Session = Depends(get_db)) -> dict:
    return {"ok": True, "data": serialize(get_note_or_404(db, note_id))}


@router.put("/{note_id}", response_model=SuccessEnvelope)
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)) -> dict:
    note = get_note_or_404(db, note_id)
    note.title = payload.title
    note.content = payload.content
    db.flush()
    db.refresh(note)
    return {"ok": True, "data": serialize(note)}


@router.delete("/{note_id}", response_model=SuccessEnvelope)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> dict:
    note = get_note_or_404(db, note_id)
    db.delete(note)
    db.flush()
    return {"ok": True, "data": {"id": note_id}}


@router.post("/{note_id}/tags", response_model=SuccessEnvelope)
def attach_tag(note_id: int, payload: NoteTagRequest, db: Session = Depends(get_db)) -> dict:
    note = get_note_or_404(db, note_id)
    tag = db.get(Tag, payload.tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    if tag not in note.tags:
        note.tags.append(tag)
        db.flush()
    return {"ok": True, "data": serialize(note)}


@router.delete("/{note_id}/tags/{tag_id}", response_model=SuccessEnvelope)
def detach_tag(note_id: int, tag_id: int, db: Session = Depends(get_db)) -> dict:
    note = get_note_or_404(db, note_id)
    tag = next((existing for existing in note.tags if existing.id == tag_id), None)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag is not attached to note")
    note.tags.remove(tag)
    db.flush()
    return {"ok": True, "data": serialize(note)}


@router.post("/{note_id}/extract", response_model=SuccessEnvelope)
def extract_note(note_id: int, apply: bool = False, db: Session = Depends(get_db)) -> dict:
    note = get_note_or_404(db, note_id)
    result = extract_content(note.content)
    if apply:
        for name in result["tags"]:
            tag = db.scalar(select(Tag).where(Tag.name == name))
            if tag is None:
                tag = Tag(name=name)
                db.add(tag)
                db.flush()
            if tag not in note.tags:
                note.tags.append(tag)
        existing_descriptions = set(db.scalars(select(ActionItem.description)).all())
        for description in result["action_items"]:
            if description not in existing_descriptions:
                db.add(ActionItem(description=description, completed=False))
                existing_descriptions.add(description)
        db.flush()
    return {"ok": True, "data": {**result, "applied": apply}}
