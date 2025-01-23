import os
from fastapi import APIRouter, Depends, HTTPException, Request
from supabase import Client
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
from database import init_supabase
from fastapi.security import OAuth2PasswordBearer
from config import Settings
import logging
from decorators import jwt_required, role_required
from database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Charger la configuration depuis un fichier externe

logger = logging.getLogger(__name__)

config=Settings.load_config()

router = APIRouter()


class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None

class GroupOut(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: datetime


@router.post("/groups/add")
async def add_group(group: GroupCreate, request:Request, db:Client = Depends(get_db)):
    data, count = db.table('groups').select('*').eq('name', group.name).execute()
    if len(data[1]) > 0:
        raise HTTPException(status_code=400, detail="Group déjà défini")

    new_group = {
        'name': group.name,
        'description': group.description
    }
    data, count = db.table('groups').insert(new_group).execute()
    return data[1][0]

@router.get("/groups/list", response_model=List[GroupOut])
@jwt_required
async def list_groups(request:Request, db:Client = Depends(get_db)):
    data, count = db.table('groups').select('*').execute()
    return data[1]

@router.delete("/groups/delete/{group}")
@jwt_required
async def delete_group(request:Request, group: int, db = Depends(get_db)):
    
    data, count = db.table('groups').delete().eq('id', group).execute()
    if count == 0:
        return {"error": "Groupe non trouvé"}
    return {"message": "Groupe supprimé avec succès"}

@router.put("/groups/update/{group_id}", response_model=GroupOut)
@jwt_required
async def update_group_route(request: Request, group_id: int, group: GroupCreate, db = Depends(init_supabase)):
    data, count = db.table('groups').update({
        'name': group.name,
        'description': group.description
    }).eq('id', group_id).execute()
    
    if count == 0:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    return data[1][0]
