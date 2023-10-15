from typing import Any

from pydantic import BaseModel, ConfigDict, Json


class DocumentCreate(BaseModel):
    """Document creation schema."""

    body: Json[Any]


class Document(BaseModel):
    """Document schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int  # noqa: A003
    body: Json[Any]
