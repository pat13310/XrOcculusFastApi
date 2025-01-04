from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from adb.adb_services_devices import AdbDevice
from decorators import jwt_required

import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class ConnectDeviceRequest(BaseModel):
    ip: str
    port: int = 5555

class DisconnectDeviceRequest(BaseModel):
    ip: str

@router.get("/devices/list")
@jwt_required
async def list_devices(request: Request):
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
@jwt_required
async def device_info(serial: str):
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
@jwt_required
async def connect_device(request: Request, connect_request: ConnectDeviceRequest):
    """Connecte un périphérique via son adresse IP et port."""
    logger.debug(f"Entrée dans la fonction connect_device avec IP={connect_request.ip}, Port={connect_request.port}")
    try:
        result = AdbDevice.connect(connect_request.ip, connect_request.port)

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
        raise HTTPException(status_code=500, detail=f"Impossible de se connecter à {connect_request.ip}:{connect_request.port} : {str(e)}")

@router.post("/devices/disconnect")
@jwt_required
async def disconnect_device(request: Request, disconnect_request: DisconnectDeviceRequest):
    """Déconnecte un périphérique spécifique par IP."""
    logger.debug(f"Entrée dans la fonction disconnect_device avec IP={disconnect_request.ip}")
    try:
        result = AdbDevice.disconnect(disconnect_request.ip)

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
        raise HTTPException(status_code=500, detail=f"Impossible de déconnecter {disconnect_request.ip} : {str(e)}")