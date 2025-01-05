from fastapi import APIRouter, HTTPException, Request
from adb.adb_services_network import AdbNetwork
from decorators import jwt_required
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/network/toggle")
@jwt_required
async def toggle(request: Request):
    """Active ou désactive le Wi-Fi."""
    logger.debug("Entrée dans la fonction toggle")
    try:
        result = AdbNetwork.toggle_wifi()
        logger.debug(f"Résultat de l'activation/désactivation du Wi-Fi : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de l'activation/désactivation du Wi-Fi : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/network/status")
async def status(request: Request):
    """Récupère le statut du Wi-Fi."""
    logger.debug("Entrée dans la fonction status")
    try:
        result = AdbNetwork.wifi_status()
        logger.debug(f"Résultat du statut du Wi-Fi : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du statut du Wi-Fi : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/network/ssid")
async def ssid(request: Request):
    """Récupère le SSID du réseau Wi-Fi connecté."""
    logger.debug("Entrée dans la fonction ssid")
    try:
        result = AdbNetwork.get_connected_ssid()
        logger.debug(f"Résultat du SSID connecté : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du SSID connecté : {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/network/ip")
async def get_ip(request: Request):
    """Récupère l'adresse IP du réseau Wi-Fi connecté."""
    logger.debug("Entrée dans la fonction get_ip")
    try:
        result = AdbNetwork.get_wifi_ip()
        logger.debug(f"Résultat de l'adresse IP du Wi-Fi : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'adresse IP du Wi-Fi : {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/network/reset")
async def reset(request: Request):
    """Réinitialise le Wi-Fi."""
    logger.debug("Entrée dans la fonction reset")
    try:
        result = AdbNetwork.reset_wifi()
        logger.debug(f"Résultat de la réinitialisation du Wi-Fi : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la réinitialisation du Wi-Fi : {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/network/signal")
async def wifi_signal_strength(request: Request):
    """Récupère la force du signal Wi-Fi."""
    logger.debug("Entrée dans la fonction wifi_signal_strength")
    try:
        result = AdbNetwork.wifi_signal_strength()
        logger.debug(f"Résultat de la force du signal Wi-Fi : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la force du signal Wi-Fi : {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/network/frequency")
async def wifi_frequency(request: Request):
    """Récupère la fréquence du Wi-Fi."""
    logger.debug("Entrée dans la fonction wifi_frequency")
    try:
        result = AdbNetwork.wifi_frequency()
        logger.debug(f"Résultat de la fréquence du Wi-Fi : {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la fréquence du Wi-Fi : {e}")
        raise HTTPException(status_code=500, detail=str(e))