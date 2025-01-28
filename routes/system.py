from fastapi import APIRouter, HTTPException, Request
from adb.adb_system import AdbSystem
import logging
from decorators import jwt_required

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/system/battery")
@jwt_required
async def battery_info(request: Request):
    """Récupère les informations sur la batterie."""
    logger.debug("Entrée dans la fonction battery_info")
    try:
        result = AdbSystem.battery_info()
        logger.debug(f"Résultat des informations sur la batterie : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des informations sur la batterie : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system/uptime")
@jwt_required
async def uptime(request: Request):
    """Récupère le temps de fonctionnement du périphérique."""
    logger.debug("Entrée dans la fonction uptime")
    try:
        result = AdbSystem.uptime()
        infos=result.split(",")
        logger.debug(f"Résultat du temps de fonctionnement : {result}")
        return {f"status":"OK", f"uptime":infos[0].strip(), f"users":infos[1].strip(),"infos":infos[2].strip()}
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du temps de fonctionnement : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system/screen")
@jwt_required
async def screen_status(request: Request):
    """Récupère l'état de l'écran."""
    logger.debug("Entrée dans la fonction screen_status")
    try:
        result = AdbSystem.screen_status()
        logger.debug(f"Résultat de l'état de l'écran : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'état de l'écran : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system/thermal")
@jwt_required
async def thermal_info(request: Request):
    """Récupère les informations thermiques."""
    logger.debug("Entrée dans la fonction thermal_info")
    try:
        result = AdbSystem.thermal_info()
        logger.debug(f"Résultat des informations thermiques : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des informations thermiques : {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/system/cpu")
@jwt_required
async def cpu_info(request: Request):
    """Récupère les informations thermiques."""
    logger.debug("Entrée dans la fonction cpu_info")
    try:
        result = AdbSystem.get_cpu_info()
        logger.debug(f"Résultat des informations cpu : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des informations cpu : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system/memory")
@jwt_required
async def memory_info(request: Request):
    """Récupère les informations mémoires."""
    logger.debug("Entrée dans la fonction memory_info")
    try:
        result = AdbSystem.memory_info()
        logger.debug(f"Résultat des informations mémoire : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des informations mémoire : {e}")
        raise HTTPException(status_code=500, detail=str(e))
    