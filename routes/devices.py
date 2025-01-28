from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from adb.adb_services_devices import AdbDevice
from decorators import jwt_required
from typing import Optional

import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class DeviceRequest(BaseModel):
    ip: str="auto"
    port: int=5555
    device: Optional[str] = None

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
async def connect_device(request: Request, connect_request: DeviceRequest):
    """Connecte un périphérique via son adresse IP et port."""
    logger.debug(f"Entrée dans la fonction connect_device avec IP={connect_request.ip}, Port={connect_request.port}")
    try:
        status="Erreur"
        if not connect_request.ip or connect_request.ip == "auto":
            if connect_request.device:
                connect_request.ip=AdbDevice.get_ip(connect_request.device)
        result = AdbDevice.connect(connect_request.ip, connect_request.port)

        if result.get("statut") == 'Erreur':
            detail=f"Erreur {result.get('message')}: {result.get('detail')}"
        elif not result:
            detail="La connexion a échoué"
        elif  result.get("statut") == 'Succès' :
            status="Succès"
            detail=f"Périphérique {connect_request.ip}:{connect_request.port} connecté avec succès"

    except HTTPException as e:
        logger.error(f"{e}")
        detail = f"{e}"

    except Exception as e:
        logger.error(f"Erreur lors de la connexion du périphérique : {e}")
        detail = f"Impossible de se connecter à {connect_request.ip}:{connect_request.port}"
    return {"status": status, "message": detail}

@router.post("/devices/disconnect")
@jwt_required
async def disconnect_device(request: Request, disconnect_request: DeviceRequest):
    """Déconnecte un périphérique spécifique par IP."""
    logger.debug(f"Entrée dans la fonction disconnect_device avec IP={disconnect_request.ip}")
    status = "Erreur"
    try:
        result = AdbDevice.disconnect(disconnect_request.ip)
        if result.get("statut") == 'Erreur':
            detail=f"{result.get('message')}"
        elif not result:
            detail="La déconnexion a échoué"
        else:
            status="Succès"
            detail=f"Périphérique {disconnect_request.ip}:{disconnect_request.port} déconnecté avec succès"

    except HTTPException as e:
        logger.error(f"{e}")
        detail = f"{e}"
        
    except Exception as e:
        logger.error(f"{e}")
        detail = f"Impossible de se déconnecter à {disconnect_request.ip}:{disconnect_request.port}"
    
    return {"status": status, "message": detail}
    
@router.post("/devices/mode/{mode}")
@jwt_required
async def disconnect_device(request: Request, mode: str):
    try:
        result = AdbDevice.set_mode(mode=mode)
        if "restarting" in result:
            return {"message": f"Mode {mode} activé"}
        if "Erreur" in result:
            raise HTTPException(status_code=400, detail=f"Aucun appareil connecté")
        if not result:            
            raise HTTPException(status_code=400, detail="La commande a échoué")
        
    except HTTPException as e:
        logger.error(f"{e}")
        raise e
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=500, detail=f"Impossible de lancer la commande  : {str(e)}")
    

    