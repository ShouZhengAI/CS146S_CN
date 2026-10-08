from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip().lstrip("#").lower()
        if not value:
            raise ValueError("tag name must not be blank")
        return value


class TagRead(ORMModel):
    id: int
    name: str


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=20_000)

    @field_validator("title", "content")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class NoteUpdate(NoteCreate):
    pass


class NoteRead(ORMModel):
    id: int
    title: str
    content: str
    created_at: datetime
    tags: list[TagRead] = Field(default_factory=list)


class ActionItemCreate(BaseModel):
    description: str = Field(min_length=1, max_length=500)

    @field_validator("description")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("description must not be blank")
        return value


class ActionItemRead(ORMModel):
    id: int
    description: str
    completed: bool


class BulkCompleteRequest(BaseModel):
    ids: list[int] = Field(min_length=1, max_length=100)

    @field_validator("ids")
    @classmethod
    def unique_positive_ids(cls, value: list[int]) -> list[int]:
        if any(item_id <= 0 for item_id in value):
            raise ValueError("ids must be positive")
        return list(dict.fromkeys(value))


class NoteTagRequest(BaseModel):
    tag_id: int = Field(gt=0)


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Any | None = None


class SuccessEnvelope(BaseModel):
    ok: bool = True
    data: Any
    error: None = None


class ErrorEnvelope(BaseModel):
    ok: bool = False
    data: None = None
    error: ErrorDetail
