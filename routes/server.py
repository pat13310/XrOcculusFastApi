from fastapi import APIRouter, HTTPException, Request
from adb.adb_services_server import AdbServer
from decorators import jwt_required
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/server/start")
@jwt_required
async def start_server(request:Request):
    """Démarre le serveur ADB."""
    logger.debug("Entrée dans la fonction start_server")
    try:
        result = AdbServer.start_server()
        logger.debug(f"Résultat du démarrage du serveur : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors du démarrage du serveur : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/server/stop")
@jwt_required
async def stop_server(request:Request):
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
@jwt_required
async def restart_server(request:Request):
    """Redémarre le serveur ADB."""
    logger.debug("Entrée dans la fonction restart_server")
    try:
        result = AdbServer.restart_server()
        logger.debug(f"Résultat du redémarrage du serveur : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors du redémarrage du serveur : {e}")
        raise HTTPException(status_code=500, detail=str(e))