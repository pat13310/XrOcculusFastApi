import os
from fastapi import APIRouter, Depends, HTTPException, Request
from supabase import Client
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
from database import init_supabase
from fastapi.security import OAuth2PasswordBearer
from config import Settings
import logging
from decorators import jwt_required, role_required

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logger = logging.getLogger(__name__)
config = Settings.load_config()
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
@jwt_required
async def add_group(group: GroupCreate, request: Request, db: Client = Depends(init_supabase)):
    data, count = db.table('groups').select('*').eq('name', group.name).execute()
    if len(data[1]) > 0:
        raise HTTPException(status_code=400, detail="Group déjà défini")

    from uuid import uuid4
    
    new_group = {
        'id': str(uuid4()),
        'name': group.name,
        'description': group.description
    }
    data, count = db.table('groups').insert(new_group).execute()
    return data[1][0]

@router.get("/groups/list", response_model=List[GroupOut])
@jwt_required
async def list_groups(request: Request, db: Client = Depends(init_supabase)):
    data, count = db.table('groups').select('*').execute()
    return data[1]

@router.delete("/groups/delete/{group_id}")
@jwt_required
async def delete_group(request: Request, group_id: str, db: Client = Depends(init_supabase)):
    data, _ = db.table('groups').delete().eq('id', group_id).execute()
    if len(data[1]) == 0 :
        return {"error": "Groupe non trouvé"}
    return {"message": "Groupe {data[1][0].name} supprimé avec succès"}

@router.put("/groups/update/{group_id}", response_model=GroupOut)
@jwt_required
async def update_group_route(request: Request, group_id: str, group: GroupCreate, db: Client = Depends(init_supabase)):
    data, count = db.table('groups').update({
        'name': group.name,
        'description': group.description
    }).eq('id', group_id).execute()
    
    if count == 0:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    return data[1][0]
