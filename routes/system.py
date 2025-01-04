from fastapi import APIRouter, HTTPException
from adb.adb_system import AdbSystem
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/system/battery")
def battery_info():
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
def uptime():
    """Récupère le temps de fonctionnement du périphérique."""
    logger.debug("Entrée dans la fonction uptime")
    try:
        result = AdbSystem.uptime()
        logger.debug(f"Résultat du temps de fonctionnement : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du temps de fonctionnement : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system/screen")
def screen_status():
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
def thermal_info():
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
def cpu_info():
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
def memory_info():
    """Récupère les informations mémoires."""
    logger.debug("Entrée dans la fonction memory_info")
    try:
        result = AdbSystem.memory_info()
        logger.debug(f"Résultat des informations mémoire : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des informations mémoire : {e}")
        raise HTTPException(status_code=500, detail=str(e))
    