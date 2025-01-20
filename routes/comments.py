from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from pydantic import BaseModel
from typing import List
import os

router = APIRouter()

# Configuration Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

security = HTTPBearer()

class CommentCreate(BaseModel):
    content: str

class Comment(BaseModel):
    id: str
    user_id: str
    content: str
    created_at: str

@router.post("/comments", response_model=Comment)
async def create_comment(
    comment: CommentCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        # Vérifier l'authentification
        user = supabase.auth.get_user(credentials.credentials)
        if not user:
            raise HTTPException(status_code=401, detail="Non authentifié")

        # Créer le commentaire
        new_comment = supabase.table("comments").insert({
            "user_id": user.user.id,
            "content": comment.content
        }).execute()

        return new_comment.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/comments", response_model=List[Comment])
async def get_comments():
    try:
        comments = supabase.table("comments").select("*").execute()
        return comments.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
