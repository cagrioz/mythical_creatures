from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from uuid import uuid4

from app.database import Base

class BaseModel(Base):
    """Base model class that includes common fields and methods."""
    __abstract__ = True

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
