from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db, engine, Base
from app.models import base as models
from app.schemas import base as schemas
from app.utils.crud import validate_uuid, get_object_or_404, delete_object, get_objects_list

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mythical Creatures API")

# Creature endpoints
@app.post("/creatures/", response_model=schemas.CreatureSimple)
def create_creature(creature: schemas.CreatureCreate, db: Session = Depends(get_db)) -> models.Creature:
    db_creature = models.Creature(**creature.model_dump())
    db.add(db_creature)
    db.commit()
    db.refresh(db_creature)
    return db_creature

@app.get("/creatures/", response_model=list[schemas.Creature])
def read_creatures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[models.Creature]:
    return get_objects_list(db, models.Creature, skip=skip, limit=limit)

@app.get("/creatures/{creature_id}", response_model=schemas.Creature)
def read_creature(creature_id: str, db: Session = Depends(get_db)) -> models.Creature:
    return get_object_or_404(db, models.Creature, creature_id)

@app.put("/creatures/{creature_id}", response_model=schemas.CreatureSimple)
def update_creature(creature_id: str, creature: schemas.CreatureCreate, db: Session = Depends(get_db)) -> models.Creature:
    db_creature = get_object_or_404(db, models.Creature, creature_id)
    db_creature.name = creature.name
    db_creature.species = creature.species
    db.commit()
    db.refresh(db_creature)
    return db_creature

@app.delete("/creatures/{creature_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_creature(creature_id: str, db: Session = Depends(get_db)) -> None:
    delete_object(db, models.Creature, creature_id)

# Realm endpoints
@app.post("/realms/", response_model=schemas.RealmSimple)
def create_realm(realm: schemas.RealmCreate, db: Session = Depends(get_db)) -> models.Realm:
    db_realm = models.Realm(**realm.model_dump())
    db.add(db_realm)
    db.commit()
    db.refresh(db_realm)
    return db_realm

@app.get("/realms/", response_model=list[schemas.Realm])
def read_realms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[models.Realm]:
    return get_objects_list(db, models.Realm, skip=skip, limit=limit)

@app.get("/realms/{realm_id}", response_model=schemas.Realm)
def read_realm(realm_id: str, db: Session = Depends(get_db)) -> models.Realm:
    return get_object_or_404(db, models.Realm, realm_id)

@app.put("/realms/{realm_id}", response_model=schemas.RealmSimple)
def update_realm(realm_id: str, realm: schemas.RealmCreate, db: Session = Depends(get_db)) -> models.Realm:
    db_realm = get_object_or_404(db, models.Realm, realm_id)
    db_realm.name = realm.name
    db.commit()
    db.refresh(db_realm)
    return db_realm

@app.delete("/realms/{realm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_realm(realm_id: str, db: Session = Depends(get_db)) -> None:
    delete_object(db, models.Realm, realm_id)

# Membership endpoints
@app.post("/memberships/", status_code=status.HTTP_201_CREATED)
def create_membership(membership: schemas.MembershipCreate, db: Session = Depends(get_db)) -> Dict[str, str]:
    validate_uuid(membership.creature_id)
    validate_uuid(membership.realm_id)
    
    creature = get_object_or_404(db, models.Creature, membership.creature_id)
    realm = get_object_or_404(db, models.Realm, membership.realm_id)
    
    if realm in creature.realms:
        raise HTTPException(status_code=400, detail="Membership already exists")
    
    creature.realms.append(realm)
    db.commit()
    return {"detail": "Membership created successfully"}

@app.delete("/memberships/", status_code=status.HTTP_204_NO_CONTENT)
def delete_membership(
    creature_id: str = Query(..., description="The ID of the creature"),
    realm_id: str = Query(..., description="The ID of the realm"),
    db: Session = Depends(get_db)
) -> None:
    validate_uuid(creature_id)
    validate_uuid(realm_id)
    
    creature = get_object_or_404(db, models.Creature, creature_id)
    realm = get_object_or_404(db, models.Realm, realm_id)
    
    if realm not in creature.realms:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    creature.realms.remove(realm)
    db.commit()

@app.get("/realms/{realm_id}/creatures/", response_model=list[schemas.CreatureSimple])
def read_realm_creatures(realm_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[models.Creature]:
    realm = get_object_or_404(db, models.Realm, realm_id)
    return realm.creatures[skip:skip + limit]
