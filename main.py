import json
import logging
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import os
from datetime import timedelta
from models.models import User
from config import load_config

# Importer le routeur auth et les fonctions utilitaires
from routes.users import router as user_router
from routes.groups import router as group_router
from routes.session import router as session_router

from auth.auth import (
    authenticate_user, 
    create_access_token,     
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from database import get_db, engine, Base, init_db

from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

# Configurer le journal
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Charger la configuration depuis un fichier externe
config = load_config()

# Initialisation de l'application FastAPI
app = FastAPI()

# Remplacer par les gestionnaires d'événements de durée de vie
@app.on_event("startup")
async def startup_event():
    init_db()

# Modèle Pydantic pour la connexion
class LoginRequest(BaseModel):
    username: str
    password: str


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Route de login
@app.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(
        db, 
        form_data.username, 
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Créer un token d'accès
    access_token_expires = timedelta(minutes=config.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    access_token = create_access_token(
        data={"sub": user.username or user.email}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name
        }
    }


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
blacklist = set()

# Créer les tables
Base.metadata.create_all(bind=engine)

# --- Dépendances ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, config.get("SECRET_KEY"), algorithms=config.get("ALGORITHM"))
        username: str = payload.get("sub")
        if username is None or token in blacklist:
            raise HTTPException(status_code=401, detail="Invalid token")
        return get_user(db, username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Inclure le routeur auth avec la dépendance db
app.include_router(user_router, dependencies=[Depends(get_db)])
app.include_router(group_router, dependencies=[Depends(get_db)])
app.include_router(session_router, dependencies=[Depends(get_db)])

# Route de logout
@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    blacklist.add(token)
    return {"message": "Déconnexion réussie"}

# Route racine
@app.get("/")
async def read_root():
    return {
        "message": "Bienvenue sur l'API XrOcculus FastAPI",
        "version": config.get("version", "1.0.0"),
        "date_de_creation": "2025-01-01",
        "auteur": "Xen"
    }

# Middleware pour gérer les erreurs 404
@app.middleware("http")
async def custom_404_handler(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": "Ressource non trouvée"})
    return response

# Gestionnaire d'erreurs personnalisé pour les erreurs HTTP
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

# Route de développement pour Swagger UI
@app.get("/dev/swagger", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger UI")

# Route de développement pour ReDoc
@app.get("/dev/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(openapi_url="/openapi.json", title="ReDoc")

# Démarrage du serveur
if __name__ == '__main__':
    import uvicorn
    logger.info("Démarrage du serveur FastAPI")
    logger.debug(f"Host: {config.get('host', '0.0.0.0')}, Port: {config.get('port', 8000)}, Reload: {config.get('reload', True)}")
    uvicorn.run("main:app", host=config.get("host", "0.0.0.0"), port=config.get("port", 8000), reload=config.get("reload", True))