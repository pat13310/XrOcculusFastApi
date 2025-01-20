from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from supabase import Client
from config import settings
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = settings.load_config()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(supabase: Client, email: str, password: str):
    """Authentifier un utilisateur avec Supabase Auth"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            logger.info(f"Authentification réussie pour : {email}")
            return response.user
        else:
            logger.warning(f"Échec de l'authentification pour : {email}")
            return None
            
    except Exception as e:
        logger.error(f"Erreur d'authentification : {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides"
        )

async def get_current_user(token: str = Depends(oauth2_scheme), supabase: Client = Depends(get_db)):
    """Obtenir l'utilisateur courant à partir du token Supabase"""
    try:
        # Vérifier le token avec Supabase
        user = supabase.auth.get_user(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user
    except Exception as e:
        logger.error(f"Erreur de vérification du token : {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def get_current_active_user(current_user = Depends(get_current_user)):
    """Vérifier si l'utilisateur est actif"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Utilisateur inactif")
    return current_user
