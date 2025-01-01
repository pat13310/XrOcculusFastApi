from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional, Dict, Union
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.models import User  # Supprimer UserInDB
import logging
import os
from sqlalchemy.orm import Session
from database import SessionLocal  # Importer la session de la base de données

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hachage du mot de passe avec des paramètres plus robustes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__default_rounds=12)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier le mot de passe avec des logs de débogage"""
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        if not result:
            logger.warning(f"Échec de la vérification du mot de passe")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la vérification du mot de passe : {e}")
        return False

def get_password_hash(password: str) -> str:
    """Générer un hachage de mot de passe sécurisé"""
    return pwd_context.hash(password)

def get_user(db: Session, username: Union[str, None] = None, email: Union[str, None] = None) -> Union[User, None]:
    """Rechercher un utilisateur par username ou email"""
    if username:
        return db.query(User).filter(User.username == username).first()
    
    if email:
        return db.query(User).filter(User.email == email).first()
    
    return None

def authenticate_user(db: Session, username: str, password: str) -> Union[User, bool]:
    """Authentifier un utilisateur avec des vérifications améliorées"""
    # Essayer d'abord avec l'email, puis avec le username
    user = get_user(db, email=username) or get_user(db, username=username)
    
    if not user:
        logger.warning(f"Utilisateur non trouvé : {username}")
        return False
    
    if not verify_password(password, user.hashed_password):
        logger.warning(f"Mot de passe incorrect pour : {username}")
        return False
    
    logger.info(f"Authentification réussie pour : {username}")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Créer un token d'accès JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
class TokenData(BaseModel):
    username: Optional[str] = None
def get_db():
    """Obtenir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Obtenir l'utilisateur courant à partir du token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide",
                headers={"WWW-Authenticate": "Bearer"}
            )
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user = get_user(db, username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Vérifier si l'utilisateur est actif"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Utilisateur inactif")
    return current_user
