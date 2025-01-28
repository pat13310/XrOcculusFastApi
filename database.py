import os
from fastapi import HTTPException
from supabase import Client
from config import settings
import logging
from typing import Optional
import jwt_test

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")  # Utiliser la clé de rôle de service
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")  # Utiliser la clé secrète JWT

# Initialisation du client Supabase
supabase: Optional[Client] = None

def init_supabase() -> Client:
    """Initialise et retourne le client Supabase"""
    global supabase
    if supabase is None:
        try:
            supabase = Client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)
            logger.info("Connexion à Supabase établie avec succès")
        except Exception as e:
            logger.error(f"Échec de la connexion à Supabase : {e}")
            raise
    return supabase

def get_db() -> Client:
    """Retourne le client Supabase pour les dépendances FastAPI"""
    return init_supabase()


def resolve_token(token: str):
    try:
        # Décoder le token en vérifiant la clé secrète et l'algorithme utilisé
        payload = jwt_test.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])

        # Récupérer l'ID utilisateur (subject 'sub' du token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Identifiant utilisateur manquant dans le token")

        return user_id

    except jwt_test.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token JWT expiré")
    except jwt_test.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token JWT invalide")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Erreur lors du décodage du token: {str(e)}")


