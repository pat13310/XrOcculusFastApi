from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from supabase import Client
from config import settings
import logging
from datetime import datetime

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

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme), supabase: Client = Depends(get_db)):
    """Obtenir l'utilisateur courant à partir du token Supabase"""
    try:
        # Vérifier si le token existe dans le localStorage
        if not token:
            token = request.cookies.get("sb-access-token")
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token manquant",
                    headers={"WWW-Authenticate": "Bearer"}
                )

        # Vérifier la date d'expiration du token
        user = supabase.auth.get_user(token)
        if user and user.expires_at:
            expiration_date = datetime.fromtimestamp(user.expires_at)
            if datetime.now() > expiration_date:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expiré",
                    headers={"WWW-Authenticate": "Bearer"}
                )
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
