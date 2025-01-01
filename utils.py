from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    hashed = pwd_context.hash(password)
    logger.debug("Mot de passe haché : %s", hashed)
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    logger.debug("Mot de passe en clair pour vérification : %s", plain_password)
    logger.debug("Mot de passe haché pour vérification : %s", hashed_password)
    return pwd_context.verify(plain_password, hashed_password)