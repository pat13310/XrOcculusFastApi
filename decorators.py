from functools import wraps
from fastapi import HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from config import load_config
from models.models import User
from database import SessionLocal

# Charger la configuration
config = load_config()

SECRET_KEY = config.get('SECRET_KEY')
ALGORITHM = config.get('ALGORITHM')

# Fonction pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📌 Décorateur pour sécuriser les routes avec JWT
def jwt_required(func):
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        token = request.headers.get("Authorization")
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token manquant",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Format du token invalide",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token invalide",
                    headers={"WWW-Authenticate": "Bearer"}
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide ou expiré",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Vérifier l'utilisateur dans la base de données
        db: Session = next(get_db())
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur introuvable",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Stocker l'utilisateur pour une utilisation ultérieure
        request.state.current_user = user
        
        return await func(*args, request=request, **kwargs)
    
    return wrapper