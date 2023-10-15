from sqlalchemy import Column, Integer
from sqlalchemy.dialects import sqlite

from src.core.database import Base


class Document(Base):
    """Model definition for documents."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    body = Column(sqlite.JSON)
