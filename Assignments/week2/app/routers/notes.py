from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from .. import db
from ..services.extract import extract_action_items_llm


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("")
def create_note(payload: Dict[str, Any]) -> Dict[str, Any]:
    content = str(payload.get("content", "")).strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
    note_id = db.insert_note(content)
    note = db.get_note(note_id)
    return {
        "id": note["id"],
        "content": note["content"],
        "created_at": note["created_at"],
    }


@router.get("")
def list_all_notes() -> List[Dict[str, Any]]:
    """Return notes newest first, matching the database ordering."""
    return [
        {"id": row["id"], "content": row["content"], "created_at": row["created_at"]}
        for row in db.list_notes()
    ]


@router.post("/extract-llm")
def extract_note_with_llm(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Use Ollama to extract tasks and optionally persist the source note."""
    text = str(payload.get("text", "")).strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id = db.insert_note(text) if payload.get("save_note") else None
    items = extract_action_items_llm(text)
    ids = db.insert_action_items(items, note_id=note_id)
    return {
        "note_id": note_id,
        "items": [{"id": item_id, "text": item} for item_id, item in zip(ids, items)],
    }


@router.get("/{note_id}")
def get_single_note(note_id: int) -> Dict[str, Any]:
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return {"id": row["id"], "content": row["content"], "created_at": row["created_at"]}


