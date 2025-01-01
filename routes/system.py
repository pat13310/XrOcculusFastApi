from fastapi import APIRouter, HTTPException
from adb.adb_services_server import AdbServer
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/start")
def start_server():
    """Démarre le serveur ADB."""
    logger.debug("Entrée dans la fonction start_server")
    try:
        result = AdbServer.start_server()
        logger.debug(f"Résultat du démarrage du serveur : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors du démarrage du serveur : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
def stop_server():
    """Arrête le serveur ADB."""
    logger.debug("Entrée dans la fonction stop_server")
    try:
        result = AdbServer.stop_server()
        logger.debug(f"Résultat de l'arrêt du serveur : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de l'arrêt du serveur : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/restart")
def restart_server():
    """Redémarre le serveur ADB."""
    logger.debug("Entrée dans la fonction restart_server")
    try:
        result = AdbServer.restart_server()
        logger.debug(f"Résultat du redémarrage du serveur : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors du redémarrage du serveur : {e}")
        raise HTTPException(status_code=500, detail=str(e))