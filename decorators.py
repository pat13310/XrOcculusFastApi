from functools import wraps
from fastapi import HTTPException, Request, status, Depends
from config import Settings
from database import init_supabase

# Charger la configuration
config = Settings.load_config()

SECRET_KEY = config.get('SECRET_KEY')
ALGORITHM = config.get('ALGORITHM')


import logging

logger = logging.getLogger(__name__)

def jwt_required(func):
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        db = init_supabase()
        try:
            token = request.cookies.get("sb-access-token") or request.headers.get("Authorization")

            if not token:
                logger.warning("Tentative d'accès sans token.")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token manquant",
                    headers={"WWW-Authenticate": "Bearer"}
                )

            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            response = db.auth.get_user(token)

            if response.user is None:
                logger.error("Token invalide fourni.")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")

            request.state.current_user = response.user
        
        except Exception as e:
            logger.exception("Erreur d'authentification JWT")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Erreur d'authentification JWT",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return await func(*args, request=request, **kwargs)
    
    return wrapper

# 📌 Décorateur pour vérifier le rôle de l'utilisateur
def role_required(required_role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            current_user = request.state.current_user
            if current_user.role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Accès refusé : rôle insuffisant"
                )
            return await func(*args, request=request, **kwargs)
        return wrapper
    return decorator
