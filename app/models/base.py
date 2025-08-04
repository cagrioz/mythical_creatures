from typing import List
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base
from app.models.base_model import BaseModel

# Association table for many-to-many relationship
membership = Table(
    'membership',
    Base.metadata,
    Column('creature_id', String, ForeignKey('creatures.id', ondelete="CASCADE")),
    Column('realm_id', String, ForeignKey('realms.id', ondelete="CASCADE")),
)

class Creature(BaseModel):
    __tablename__ = "creatures"

    name: Mapped[str] = mapped_column(String, nullable=False)
    species: Mapped[str] = mapped_column(String, nullable=False)
    
    # Relationship with realms
    realms: Mapped[List["Realm"]] = relationship("Realm", secondary=membership, back_populates="creatures")

class Realm(BaseModel):
    __tablename__ = "realms"

    name: Mapped[str] = mapped_column(String, nullable=False)
    
    # Relationship with creatures
    creatures: Mapped[List["Creature"]] = relationship("Creature", secondary=membership, back_populates="realms")
