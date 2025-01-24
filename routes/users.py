from fastapi import APIRouter, Depends, HTTPException, Request
from datetime import datetime
import logging
from supabase import Client
from database import get_db
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()


# --- Fonctions Utilitaires ---
def get_user(username: str, db: Client = Depends(get_db)):
    response = db.table('users').select('*').eq('username', username).execute()
    return response.data[0] if response.data else None

def add_profile(user_id: str, fullname: str, db: Client = Depends(get_db)):
    """Ajoute un profil utilisateur dans la table profiles"""
    profile_data = {
        "id": user_id,
        "username": fullname.lower().replace(" ", "_"),
        "created_at": datetime.utcnow().isoformat()
    }
    
    try:
        response = db.table('profiles').insert(profile_data).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Erreur lors de la création du profil")
    except Exception as e:
        logger.error(f"Erreur création profil: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la création du profil")


# --- Routes ---
@router.post("/users/add")
async def add_user(request: Request, db: Client = Depends(get_db)):
    user = await request.json()
    print(type(user))
    # Vérification des credentials via Supabase Auth
    try:
        response = db.auth.sign_in_with_password({
            "email": user['email'],
            "password": user['password']
        })
        if response.user:
            return HTTPException(status_code=400, detail="Utilisateur déjà enregistré")
    except Exception as e:
        logger.error(f"Erreur d'authentification: {str(e)}")
        #raise HTTPException(status_code=401, detail="Email ou mot de passe invalide")
    
    # Création de l'utilisateur via Supabase Auth
    try:
        sign_up_response = db.auth.sign_up({
            "email": user['email'],
            "password": user['password'],
            "options": {
                "data": {
                    "username": user['username'],
                    "full_name": user.get('full_name'),
                    "role": user.get('role'),
                    "group": user.get('group')
                }
            }
        })
        
        if sign_up_response.user:
            # Création du profil associé
            profile = add_profile(
                user_id=sign_up_response.user.id,
                fullname=user.get('full_name', user['username']),
                db=db
            )
            
            return {
                "id": sign_up_response.user.id,
                "email": sign_up_response.user.email,
                "username": user['username'],
                "role": user.get('role'),
                "group": user.get('group'),
                "profile": profile
            }
        raise HTTPException(status_code=400, detail="Erreur lors de la création de l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur lors de l'inscription: {str(e)}")
        raise HTTPException(status_code=400, detail="Erreur lors de la création de l'utilisateur")

@router.get("/users/list")
async def list_users(request: Request, db: Client = Depends(get_db)):
    response = db.auth.admin.list_users()
    return response

@router.get("/users/find/byId/{user_id}")
async def find_user_by_id(user_id: str, db: Client = Depends(get_db)):
    """Trouve un utilisateur par son ID avec son profil associé"""
    try:
        # Validation de l'UUID
        uuid.UUID(user_id)
        
        # Récupération de l'utilisateur
        user = db.auth.admin.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
            
        # Récupération du profil
        profile = db.table('profiles').select('*').eq('id', user_id).execute()
        
        return {
            "user": user,
            "profile": profile.data[0] if profile.data else None
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="ID utilisateur invalide")
    except Exception as e:
        logger.error(f"Erreur recherche utilisateur: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la recherche")

@router.get("/users/me")
async def get_current_user(db: Client = Depends(get_db)):
    """Récupère l'utilisateur actuellement authentifié"""
    try:
        # Récupération de l'utilisateur via le token JWT
        user = db.auth.get_user()
        if not user:
            raise HTTPException(status_code=401, detail="Non authentifié")
            
        # Récupération du profil associé
        profile = db.table('profiles').select('*').eq('id', user.user.id).execute()
        
        return {
            "user": user.user,
            "profile": profile.data[0] if profile.data else None
        }
    except Exception as e:
        logger.error(f"Erreur récupération utilisateur: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la récupération")

@router.delete("/users/delete/{user_id}")
async def delete_user(request: Request, user_id: str, db: Client = Depends(get_db)):
    try:
        # Validation de l'UUID
        uuid.UUID(user_id)
        db.auth.admin.delete_user(str(user_id))
        return {"message": f"Utilisateur supprimé avec l'id : {user_id}"}
    except ValueError:
        raise HTTPException(status_code=400, detail=f"L'ID {user_id} utilisateur doit être un identifiant valide au format UUID")
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de l'utilisateur: {str(e)}")
        return {"error": "Utilisateur non trouvé avec l'ID fourni"}

@router.put("/users/update/{user_id}")
async def update_user_route(request: Request, user_id: str, db: Client = Depends(get_db)):
    user = await request.json()
    existing_user = db.table('users').select('*').eq('id', user_id).execute()
    if not existing_user.data:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    updates = {}
    if 'username' in user: updates['username'] = user['username']
    if 'email' in user: updates['email'] = user['email']
    if 'full_name' in user: updates['full_name'] = user['full_name']
    if 'password' in user: updates['password'] = user['password']
    if 'role' in user: updates['role'] = user['role']
    if 'group' in user: updates['group'] = user['group']
    updates['updated_at'] = datetime.utcnow().isoformat()
    
    response = db.table('users').update(updates).eq('id', user_id).execute()
    return response.data[0]
