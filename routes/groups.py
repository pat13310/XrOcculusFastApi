import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
from database import get_db
from utils import hash_password, verify_password
from fastapi.security import OAuth2PasswordBearer
from config import Settings
import logging
from decorators import jwt_required, role_required


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Charger la configuration depuis un fichier externe

logger = logging.getLogger(__name__)

config=Settings.load_config()

router = APIRouter()


class GroupCreate(BaseModel):
    name: str

class GroupOut(BaseModel):
    id: int
    name: str


@router.post("/groups/add", response_model=GroupOut)
async def add_group( request:Request, group: GroupCreate, db: Session = Depends(get_db)):
    existing_group = db.query(Group).filter(Group.name == group.name).first()
    if existing_group:
        raise HTTPException(status_code=400, detail="Group déjà défini")

    new_group = Group(name=group.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

@router.get("/groups/list", response_model=List[GroupOut])
@jwt_required
async def list_groups(request:Request,  db: Session = Depends(get_db)):
    groups = db.query(Group).all()
    return groups

@router.delete("/groups/delete/{group}")
@jwt_required
@role_required("admin")
async def delete_group(request:Request,group: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group).first()
    if not group:
        return {"error": "Groupe non trouvé"}
    db.delete(group)
    db.commit()
    return group

@router.put("/groups/update/{group_id}", response_model=GroupOut)
@jwt_required
@role_required("admin")
async def update_group_route(request: Request, group_id: int, group: GroupCreate, db: Session = Depends(get_db)):
    existing_group = db.query(Group).filter(Group.id == group_id).first()
    if not existing_group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    if group.name:
        existing_group.name = group.name
    
    db.commit()
    db.refresh(existing_group)
    return existing_group