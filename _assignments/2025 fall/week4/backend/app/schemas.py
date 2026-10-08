from pydantic import BaseModel, ConfigDict, Field, field_validator


class NonBlankModel(BaseModel):
    @field_validator("*", mode="after")
    @classmethod
    def reject_blank_strings(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("must not be blank")
        return value


class NoteCreate(NonBlankModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10_000)


class NoteUpdate(NoteCreate):
    """Complete replacement payload for an existing note."""


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str


class ActionItemCreate(NonBlankModel):
    description: str = Field(min_length=1, max_length=2_000)


class ActionItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    completed: bool
