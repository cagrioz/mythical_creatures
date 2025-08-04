from typing import TypeVar, Type, List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

def validate_uuid(id_str: str) -> None:
    """Validate that a string is a valid UUID format."""
    try:
        UUID(id_str)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format")

def get_object_or_404(db: Session, model: Type[ModelType], id: str) -> ModelType:
    """Get an object by ID or raise 404 if not found."""
    validate_uuid(id)
    obj = db.query(model).filter(model.id == id).first()
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} not found"
        )
    return obj

def delete_object(db: Session, model: Type[ModelType], id: str) -> None:
    """Delete an object by ID."""
    obj = get_object_or_404(db, model, id)
    db.delete(obj)
    db.commit()

def get_objects_list(
    db: Session,
    model: Type[ModelType],
    *,
    skip: int = 0,
    limit: int = 100
) -> List[ModelType]:
    """Get a paginated list of objects."""
    return db.query(model).offset(skip).limit(limit).all()
