import os
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from config import Settings
import logging
from decorators import jwt_required, role_required

# Configuration OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Charger la configuration depuis un fichier externe
config = Settings.load_config()

# Configurer le logger
logger = logging.getLogger(__name__)

# Initialiser le routeur FastAPI
router = APIRouter()

# Route pour ajouter une nouvelle session
@router.post("/sessions/add")
async def add_session(request: Request, db: Session = Depends(get_db)):
    existing_session = None
    if existing_session:
        raise HTTPException(status_code=400, detail="Session déjà définie")

    
    return None

# Route pour lister toutes les sessions
@router.get("/sessions/list")
async def list_sessions(request: Request, db: Session = Depends(get_db)):
    return None

# Route pour supprimer une session par ID
@router.delete("/sessions/delete/{session_id}")
async def delete_session(request: Request, session_id: int, db: Session = Depends(get_db)):
    session = None
    if not session:
        return {"error": "Session non trouvée"}
    return session

# Route pour arrêter une session par ID
@router.get("/sessions/stop/{session_id}")
async def stop_session(request: Request, session_id: int, db: Session = Depends(get_db)):
    session = None
    return session

# Route pour démarrer une session par ID
@router.get("/sessions/start/{session_id}")
async def start_session(request: Request, session_id: int, db: Session = Depends(get_db)):
    session =None
    if not session:
        raise HTTPException(status_code=400, detail="Session non trouvée")
    
    if session.state == "active":
        raise HTTPException(status_code=400, detail="La session est déjà active")

    session.state = "active"
    return session

# Route pour associer un utilisateur à une session
@router.post("/sessions/{session_id}/link/{user_id}")
async def add_user_to_session(request: Request, session_id: int, user_id: int, db: Session = Depends(get_db)):
    session =None
    if user_id == -1 or user_id==0:
        raise HTTPException(status_code=400, detail="ID utilisateur invalide")
    if not session:
        raise HTTPException(status_code=400, detail="Session non trouvée")

    user = None
    if not user:
        raise HTTPException(status_code=400, detail="Utilisateur non trouvé")

    if user in session.users:
        raise HTTPException(status_code=400, detail="Utilisateur déjà associé à la session")

    return {"message": "Utilisateur ajouté à la session avec succès"}

# Route pour dissocier un utilisateur d'une session
@router.delete("/sessions/{session_id}/unlink/{user_id}")
async def unlink_user_from_session(request: Request, session_id: int, user_id: int, db: Session = Depends(get_db)):
    session = None
    if not session:
        raise HTTPException(status_code=400, detail="Session non trouvée")

    user = None
    if not user:
        raise HTTPException(status_code=400, detail="Utilisateur non trouvé")

    if user not in session.users:
        raise HTTPException(status_code=400, detail="Utilisateur non associé à la session")

    return {"message": "Utilisateur dissocié de la session avec succès"}
