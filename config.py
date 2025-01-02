import logging
import json
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_config():
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
            "ACCESS_TOKEN_EXPIRE_MINUTES": 300
        }
    return config