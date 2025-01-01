from fastapi import APIRouter, HTTPException
from adb.adb_services_devices import AdbDevice
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
def list_devices():
    """Liste les périphériques connectés via ADB."""
    logger.debug("Entrée dans la fonction list_devices")
    try:
        devices = AdbDevice.list_devices()
        logger.debug(f"Périphériques détectés : {devices}")
        return {"devices": devices}
    except Exception as e:
        logger.error(f"Erreur lors de la liste des périphériques : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{serial}")
def device_info(serial: str):
    """Récupère les informations d'un périphérique spécifique via ADB."""
    logger.debug(f"Entrée dans la fonction device_info avec serial={serial}")
    try:
        info = AdbDevice.device_info(serial)
        logger.debug(f"Informations du périphérique {serial} : {info}")
        return info
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des informations du périphérique : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/connect")
def connect_device(ip: str, port: int = 5555):
    """Connecte un périphérique via son adresse IP et port."""
    logger.debug(f"Entrée dans la fonction connect_device avec IP={ip}, Port={port}")
    try:
        result = AdbDevice.connect(ip, port)
        logger.debug(f"Résultat de la connexion : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la connexion du périphérique : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/disconnect")
def disconnect_device(ip: str):
    """Déconnecte un périphérique spécifique par IP."""
    logger.debug(f"Entrée dans la fonction disconnect_device avec IP={ip}")
    try:
        result = AdbDevice.disconnect(ip)
        logger.debug(f"Résultat de la déconnexion : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la déconnexion du périphérique : {e}")
        raise HTTPException(status_code=500, detail=str(e))