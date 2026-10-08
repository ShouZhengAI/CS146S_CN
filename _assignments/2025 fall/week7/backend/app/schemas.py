from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator, model_validator


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class TagCreate(ApiModel):
    name: str = Field(min_length=1, max_length=50, pattern=r"^[A-Za-z0-9_-]+$")


class TagRead(TagCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid", str_strip_whitespace=True)


def normalize_tags(tags: list[str] | None) -> list[str] | None:
    if tags is None:
        return None
    cleaned = [tag.strip().lstrip("#") for tag in tags]
    if any(not tag or len(tag) > 50 for tag in cleaned):
        raise ValueError("tags must contain names between 1 and 50 characters")
    if any(not all(char.isalnum() or char in "_-" for char in tag) for tag in cleaned):
        raise ValueError("tags may only contain letters, numbers, underscores, and hyphens")
    if len({tag.lower() for tag in cleaned}) != len(cleaned):
        raise ValueError("tags must be unique")
    return cleaned


class NoteCreate(ApiModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=20_000)
    tags: list[str] = Field(default_factory=list, max_length=20)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags: list[str]) -> list[str]:
        return normalize_tags(tags) or []


class NoteRead(ApiModel):
    id: int
    title: str
    content: str
    tags: list[TagRead]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid", str_strip_whitespace=True)


class NotePatch(ApiModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1, max_length=20_000)
    tags: list[str] | None = Field(default=None, max_length=20)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags: list[str] | None) -> list[str] | None:
        return normalize_tags(tags)

    @model_validator(mode="after")
    def require_change(self) -> "NotePatch":
        if not self.model_fields_set or all(
            getattr(self, field) is None for field in ("title", "content", "tags")
        ):
            raise ValueError("at least one non-null field is required")
        return self


class ActionItemCreate(ApiModel):
    description: str = Field(min_length=1, max_length=2_000)
    completed: StrictBool = False


class ActionItemRead(ApiModel):
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid", str_strip_whitespace=True)


class ActionItemPatch(ApiModel):
    description: str | None = Field(default=None, min_length=1, max_length=2_000)
    completed: StrictBool | None = None

    @model_validator(mode="after")
    def require_change(self) -> "ActionItemPatch":
        if not self.model_fields_set or all(
            getattr(self, field) is None for field in ("description", "completed")
        ):
            raise ValueError("at least one non-null field is required")
        return self


