import os
from fastapi import APIRouter, Depends, HTTPException, Request
from datetime import datetime
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")  # Utiliser la clé de rôle de service

# Vérifier que les configurations sont chargées
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE:
    raise ValueError("Les variables d'environnement SUPABASE_URL ou SUPABASE_SERVICE_ROLE ne sont pas définies.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

router = APIRouter()


# --- Fonctions Utilitaires ---
def get_user(username: str):
    response = supabase.table('users').select('*').eq('username', username).execute()
    return response.data[0] if response.data else None


# --- Routes ---
@router.post("/users/add")
async def add_user(request: Request):
    
    existing_email = supabase.table('users').select('*').eq('email', user.email).execute()
    if existing_email.data:
        raise HTTPException(status_code=400, detail="Utilisateur déjà enregistré")
    
    user=supabase.sign_up(user.email, user.password)

    if not user:
        return {"error": "Utilisateur non rencontré"}
    
    new_user = {
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'password': user.password,
        'role': user.role,
        'group': user.group,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    return user

@router.get("/users/list")
async def list_users(request: Request):
    response = supabase.table('users').select('*').execute()
    return response.data

@router.delete("/users/delete/{user_id}")
async def delete_user(request: Request, user_id: str):
    response = supabase.table('users').delete().eq('id', user_id).execute()
    if not response.data:
        return {"error": "Utilisateur non trouvé"}
    return {"message": f"Utilisateur supprimé avec l'id : {user_id}"}

@router.put("/users/update/{user_id}")
async def update_user_route(request: Request, user_id: str):
    user = await request.json()
    existing_user = supabase.table('users').select('*').eq('id', user_id).execute()
    if not existing_user.data:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    updates = {}
    if user.username: updates['username'] = user.username
    if user.email: updates['email'] = user.email
    if user.full_name: updates['full_name'] = user.full_name
    if user.password: updates['password'] = user.password
    if user.role: updates['role'] = user.role
    if user.group is not None: updates['group'] = user.group
    updates['updated_at'] = datetime.utcnow().isoformat()
    
    response = supabase.table('users').update(updates).eq('id', user_id).execute()
    return response.data[0]
