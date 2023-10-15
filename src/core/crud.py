from sqlalchemy.orm import Session

from . import models, schemas


def get_document(db: Session, document_id: int) -> models.Document | None:
    """Return document matching identifier."""
    return db.query(models.Document).get(document_id)


def create_document(db: Session, document: schemas.DocumentCreate) -> models.Document:
    """Create a new document."""
    doc = models.Document(body=document.body)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc
