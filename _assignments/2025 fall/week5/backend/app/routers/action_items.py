from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import ActionItemCreate, ActionItemRead, BulkCompleteRequest, SuccessEnvelope

router = APIRouter(prefix="/action-items", tags=["action_items"])


def serialize(item: ActionItem) -> dict:
    return ActionItemRead.model_validate(item).model_dump()


@router.get("", response_model=SuccessEnvelope)
@router.get("/", response_model=SuccessEnvelope, include_in_schema=False)
def list_items(
    completed: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    query = select(ActionItem)
    count_query = select(func.count(ActionItem.id))
    if completed is not None:
        query = query.where(ActionItem.completed == completed)
        count_query = count_query.where(ActionItem.completed == completed)
    total = db.scalar(count_query) or 0
    rows = db.scalars(
        query.order_by(ActionItem.id.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
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
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> dict:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return {"ok": True, "data": serialize(item)}


@router.post("/bulk-complete", response_model=SuccessEnvelope)
def bulk_complete(payload: BulkCompleteRequest, db: Session = Depends(get_db)) -> dict:
    items = db.scalars(select(ActionItem).where(ActionItem.id.in_(payload.ids))).all()
    found = {item.id for item in items}
    missing = [item_id for item_id in payload.ids if item_id not in found]
    if missing:
        raise HTTPException(status_code=404, detail=f"Action items not found: {missing}")
    for item in items:
        item.completed = True
    db.flush()
    return {
        "ok": True,
        "data": {"items": [serialize(item) for item in items], "updated": len(items)},
    }


@router.put("/{item_id}/complete", response_model=SuccessEnvelope)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> dict:
    item = db.get(ActionItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.flush()
    db.refresh(item)
    return {"ok": True, "data": serialize(item)}
