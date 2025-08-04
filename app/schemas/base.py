from pydantic import BaseModel
from typing import List

# Base schemas
class CreatureBase(BaseModel):
    name: str
    species: str

class RealmBase(BaseModel):
    name: str

# Create schemas (for input)
class CreatureCreate(CreatureBase):
    pass

class RealmCreate(RealmBase):
    pass

# Simple response schemas (without relationships)
class CreatureSimple(CreatureBase):
    id: str
    
    class Config:
        from_attributes = True

class RealmSimple(RealmBase):
    id: str
    
    class Config:
        from_attributes = True

# Full response schemas (with relationships)
class Creature(CreatureBase):
    id: str
    realms: List[RealmSimple] = []  # Use RealmSimple to avoid nesting
    
    class Config:
        from_attributes = True

class Realm(RealmBase):
    id: str
    creatures: List[CreatureSimple] = []  # Use CreatureSimple to avoid nesting
    
    class Config:
        from_attributes = True

class MembershipCreate(BaseModel):
    creature_id: str
    realm_id: str
