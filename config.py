import logging
import json
from typing import Dict, Any
from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    SECRET_KEY: str = "rzrljz!-erjvncxvassssswwwwppcc!:ùlç;"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300

    class DatabaseSettings(BaseSettings):
        URL: str = "postgresql+asyncpg://postgres:your_password@db.wfbcqtwdsapqmztgcpcn.supabase.co:5432/postgres"
        TEST_URL: str = "sqlite:///:memory:"
        TEST_MODE: bool = False

    DATABASE: DatabaseSettings = DatabaseSettings()

    
    
    @staticmethod
    def load_config():
        config: Dict[str, Any]
        try:
            with open('config.json') as config_file:
                config = json.load(config_file)
                logger.debug(f"Configuration chargée: {config}")
        except FileNotFoundError:
            logger.error("Le fichier config.json est introuvable. Utilisation des valeurs par défaut.")
            config = {
            "host": "0.0.0.0",
            "port": 8000,
            "reload": True,
            "SECRET_KEY": "rzrljz!-erjvncxvassssswwwwppcc!:ùlç;",
            "ALGORITHM": "HS256",
            "ACCESS_TOKEN_EXPIRE_MINUTES": 300,
            "DATABASE": {
                "URL": "sqlite:///./app.db",
                "TEST_URL": "sqlite:///:memory:",
                "TEST_MODE": False
                }        
            }
        finally:
            return config
        
settings = Settings()
