from src.core.database import Base  # Re-export for full metadata init

from .document import Document

__all__ = ("Document", "Base")
