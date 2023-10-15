from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from config import settings

_connect_args: dict[str, Any] = {}

if settings.DATABASE_URL.startswith("sqlite://"):
    _connect_args.setdefault("check_same_thread", False)

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=_connect_args,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session() -> Session:
    """Get a new database session."""
    return SessionLocal()
