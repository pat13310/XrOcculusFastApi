import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
from database import get_db
from utils import hash_password, verify_password
from fastapi.security import OAuth2PasswordBearer
from routes.config import load_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Charger la configuration depuis un fichier externe
config = load_config()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.get('SECRET_KEY'),algorithms=config.get('ALGORITHM'))
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user
from jose import jwt
import logging
from models.models import User, Group

logger = logging.getLogger(__name__)

config=load_config()

router = APIRouter()

# --- Modèle Pydantic ---
class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    role: Optional[str] = "user"
    group: Optional[int] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    disabled: bool
    role: str
    group: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

class GroupCreate(BaseModel):
    name: str

class GroupOut(BaseModel):
    id: int
    name: str

# --- Fonctions Utilitaires ---
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if user:
        logger.debug("Utilisateur trouvé : %s", username)
        logger.debug("Mot de passe en clair : %s", password)
        logger.debug("Mot de passe haché stocké : %s", user.hashed_password)
        if verify_password(password, user.hashed_password):
            logger.debug("Mot de passe vérifié avec succès pour l'utilisateur : %s", username)
            return user
        else:
            logger.debug("Échec de la vérification du mot de passe pour l'utilisateur : %s", username)
    else:
        logger.debug("Utilisateur non trouvé : %s", username)
    return None

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, config.get("SECRET_KEY"), algorithm=config.get("ALGORITHM"))

# --- Routes ---
@router.post("/users", response_model=UserOut)
async def add_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        logger.warning("Tentative d'ajout d'un utilisateur existant : %s", user.username)
        raise HTTPException(status_code=400, detail="Utilisateur existe déjà")
    
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        logger.warning("Tentative d'ajout d'un email existant : %s", user.email)
        raise HTTPException(status_code=400, detail="Email déjà enregistré")

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role,
        group=user.group,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users", response_model=List[UserOut])
async def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.delete("/users/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "Utilisateur non trouvé"}
    db.delete(user)
    db.commit()
    return {"message": f"Utilisateur '{user.username}' supprimé avec l'id : {user_id}"}


@router.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/groups", response_model=GroupOut)
async def add_group(group: GroupCreate, db: Session = Depends(get_db)):
    existing_group = db.query(Group).filter(Group.name == group.name).first()
    if existing_group:
        raise HTTPException(status_code=400, detail="Group already registered")

    new_group = Group(name=group.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

@router.get("/groups", response_model=List[GroupOut])
async def list_groups(db: Session = Depends(get_db)):
    groups = db.query(Group).all()
    return groups

@router.delete("/groups/delete/{group}")
async def delete_group(group: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group).first()
    if not group:
        return {"error": "Groupe non trouvé"}
    db.delete(group)
    db.commit()
    return group