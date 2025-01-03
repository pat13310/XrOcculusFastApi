import os
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
from database import get_db
from models.models import Session, User
from fastapi.security import OAuth2PasswordBearer
from config import load_config
import logging
from decorators import jwt_required

# Configuration OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Charger la configuration depuis un fichier externe
config = load_config()

# Configurer le logger
logger = logging.getLogger(__name__)

# Initialiser le routeur FastAPI
router = APIRouter()

# Modèle Pydantic pour la création d'une session
class SessionCreate(BaseModel):
    name: str
    created_at: datetime
    ended_at: Optional[datetime] = None
    state: str

# Modèle Pydantic pour la sortie d'une session
class SessionOut(BaseModel):
    id: int
    name: str
    created_at: datetime
    ended_at: Optional[datetime] = None
    state: str

# Route pour ajouter une nouvelle session
@router.post("/sessions", response_model=SessionOut)
@jwt_required
async def add_session(request: Request, session: SessionCreate, db: Session = Depends(get_db)):
    existing_session = db.query(Session).filter(Session.name == session.name).first()
    if existing_session:
        raise HTTPException(status_code=400, detail="Session déjà définie")

    new_session = Session(
        name=session.name,
        created_at=datetime.utcnow(),  # Mettre à jour created_at à la date actuelle
        ended_at=session.ended_at if session.ended_at else None,
        state="active"  # Mettre à jour state à "active"
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

# Route pour lister toutes les sessions
@router.get("/sessions", response_model=List[SessionOut])
@jwt_required
async def list_sessions(request: Request, db: Session = Depends(get_db)):
    sessions = db.query(Session).all()
    return sessions

# Route pour supprimer une session par ID
@router.delete("/sessions/delete/{session_id}")
@jwt_required
async def delete_session(request: Request, session_id: int, db: Session = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session).first()
    if not session:
        return {"error": "Session non trouvée"}
    db.delete(session)
    db.commit()
    return session

# Route pour arrêter une session par ID
@router.get("/sessions/stop/{session_id}")
@jwt_required
async def stop_session(request: Request, session_id: int, db: Session = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    
    session.ended_at = datetime.utcnow()
    session.state = "inactive"
    db.commit()
    db.refresh(session)
    return session

# Route pour associer un utilisateur à une session
@router.post("/sessions/{session_id}/add_user/{user_id}")
@jwt_required
async def add_user_to_session(request: Request, session_id: int, user_id: int, db: Session = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session non trouvée")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    session.users.append(user)
    db.commit()
    return {"message": "Utilisateur ajouté à la session avec succès"}

