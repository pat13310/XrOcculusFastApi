import os
from supabase import Client
from config import settings
import logging
from typing import Optional
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
