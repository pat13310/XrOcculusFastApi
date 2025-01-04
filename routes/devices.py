from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from adb.adb_services_devices import AdbDevice
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class ConnectDeviceRequest(BaseModel):
    ip: str
    port: int = 5555

@router.get("/devices/list")
def list_devices():
    """Liste les périphériques connectés via ADB."""
    logger.debug("Entrée dans la fonction list_devices")
    try:
        devices = AdbDevice.list_devices()
        logger.debug(f"Périphériques détectés : {devices}")
        return {"devices": devices}
    except Exception as e:
        logger.error(f"Erreur lors de la liste des périphériques : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la liste des périphériques")

@router.get("/devices/{serial}")
def device_info(serial: str):
    """Récupère les informations d'un périphérique spécifique via ADB."""
    logger.debug(f"Entrée dans la fonction device_info avec serial={serial}")
    try:
        info = AdbDevice.device_info(serial)
        logger.debug(f"Informations du périphérique {serial} : {info}")
        return info
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des informations du périphérique : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des informations du périphérique")

@router.post("/devices/connect")
def connect_device(request: ConnectDeviceRequest):
    """Connecte un périphérique via son adresse IP et port."""
    logger.debug(f"Entrée dans la fonction connect_device avec IP={request.ip}, Port={request.port}")
    try:
        result = AdbDevice.connect(request.ip, request.port)

        if result.get("statut") == 'Erreur':
            raise HTTPException(status_code=400, detail=f"Erreur {result.get('message')}: {result.get('detail')}")
        if not result:
            raise HTTPException(status_code=400, detail="La connexion a échoué")
        return {"message": "Périphérique connecté avec succès"}
    except HTTPException as e:
        logger.error(f"Erreur lors de la connexion du périphérique : {e}")
        raise e
    except Exception as e:
        logger.error(f"Erreur lors de la connexion du périphérique : {e}")
        raise HTTPException(status_code=500, detail=f"Impossible de se connecter à {request.ip}:{request.port} : {str(e)}")

class DisconnectDeviceRequest(BaseModel):
    ip: str

@router.post("/devices/disconnect")
def disconnect_device(request: DisconnectDeviceRequest):
    """Déconnecte un périphérique spécifique par IP."""
    logger.debug(f"Entrée dans la fonction disconnect_device avec IP={request.ip}")
    try:
        result = AdbDevice.disconnect(request.ip)

        if result.get("statut") == 'Erreur':
            raise HTTPException(status_code=400, detail=f"{result.get('message')}")
        if not result:
            raise HTTPException(status_code=400, detail="La déconnexion a échoué")
        return {"message": "Périphérique déconnecté avec succès"}
    except HTTPException as e:
        logger.error(f"{e}")
        raise e
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=500, detail=f"Impossible de déconnecter {request.ip} : {str(e)}")