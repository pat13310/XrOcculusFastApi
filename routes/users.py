from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
from database import get_db
from utils import hash_password, verify_password
from fastapi.security import OAuth2PasswordBearer
from config import load_config

from jose import jwt
import logging
from models.models import User
from decorators import jwt_required, role_required


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
@router.post("/users/add", response_model=UserOut)
@jwt_required
@role_required("admin")
async def add_user(request:Request, user: UserCreate, db: Session = Depends(get_db)):
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


@router.get("/users/list", response_model=List[UserOut])
@jwt_required
async def list_users(request:Request,db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.delete("/users/delete/{user_id}")
@jwt_required
@role_required("admin")
async def delete_user(request:Request,user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "Utilisateur non trouvé"}
    db.delete(user)
    db.commit()
    return {"message": f"Utilisateur '{user.username}' supprimé avec l'id : {user_id}"}


@router.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/users/update/{user_id}", response_model=UserOut)
@jwt_required
@role_required("admin")
async def update_user_route(request: Request, user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    if user.username:
        existing_user.username = user.username
    if user.email:
        existing_user.email = user.email
    if user.full_name:
        existing_user.full_name = user.full_name
    if user.password:
        existing_user.hashed_password = hash_password(user.password)
    if user.role:
        existing_user.role = user.role
    if user.group is not None:
        existing_user.group = user.group
    
    existing_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(existing_user)
    return existing_user