import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Utiliser une variable d'environnement avec une valeur par défaut
DATABASE_URL = os.getenv('DATABASE_URL', "sqlite:///./app.db")

# Configuration robuste de l'engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    pool_size=10,  # Nombre maximal de connexions dans le pool
    max_overflow=20,  # Nombre de connexions supplémentaires autorisées
    echo=False  # Activer pour le débogage SQL
)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

@contextmanager
def get_db_session() -> Session:
    """Gestionnaire de contexte pour les sessions de base de données"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Erreur de transaction de base de données : {e}")
        raise
    finally:
        session.close()

def get_db():
    """Générateur de session pour les dépendances FastAPI"""
    with get_db_session() as db:
        yield db

def init_db():
    """Initialiser la base de données"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Base de données initialisée avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de la base de données : {e}")
        raise
