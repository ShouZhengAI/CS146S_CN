from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from ..db import get_db
from ..models import Tag
from ..schemas import SuccessEnvelope, TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["tags"])


def serialize(tag: Tag) -> dict:
    return TagRead.model_validate(tag).model_dump()


@router.get("", response_model=SuccessEnvelope)
@router.get("/", response_model=SuccessEnvelope, include_in_schema=False)
def list_tags(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    total = db.scalar(select(func.count(Tag.id))) or 0
    tags = db.scalars(
        select(Tag)
        .order_by(Tag.name)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return {
        "ok": True,
        "data": {
            "items": [serialize(tag) for tag in tags],
            "total": total,
            "page": page,
            "page_size": page_size,
        },
    }


@router.post("", response_model=SuccessEnvelope, status_code=201)
@router.post("/", response_model=SuccessEnvelope, status_code=201, include_in_schema=False)
def create_tag(payload: TagCreate, db: Session = Depends(get_db)) -> dict:
    if db.scalar(select(Tag).where(Tag.name == payload.name)) is not None:
        raise HTTPException(status_code=409, detail="Tag already exists")
    tag = Tag(name=payload.name)
    db.add(tag)
    db.flush()
    db.refresh(tag)
    return {"ok": True, "data": serialize(tag)}


@router.delete("/{tag_id}", response_model=SuccessEnvelope)
def delete_tag(tag_id: int, db: Session = Depends(get_db)) -> dict:
    tag = db.scalar(select(Tag).options(selectinload(Tag.notes)).where(Tag.id == tag_id))
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag.notes.clear()
    db.delete(tag)
    db.flush()
    return {"ok": True, "data": {"id": tag_id}}
