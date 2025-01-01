from fastapi import APIRouter, HTTPException
from adb.adb_services_applications import AdbApplications
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/install")
def install_application(apk_path: str):
    """Installe une application à partir d'un fichier APK."""
    logger.debug(f"Entrée dans la fonction install_application avec apk_path={apk_path}")
    if not os.path.isfile(apk_path) or not apk_path.endswith('.apk'):
        logger.warning(f"Chemin APK invalide: {apk_path}")
        raise HTTPException(status_code=400, detail=f"Le chemin APK '{apk_path}' est invalide ou le fichier n'existe pas.")
    result = AdbApplications.install(apk_path)
    logger.debug(f"Résultat de l'installation: {result}")
    return result

@router.post("/uninstall")
def uninstall_application(package_name: str):
    """Désinstalle une application en utilisant son nom de package."""
    logger.debug(f"Entrée dans la fonction uninstall_application avec package_name={package_name}")
    result = AdbApplications.uninstall(package_name)
    logger.debug(f"Résultat de la désinstallation: {result}")
    return result

@router.get("/list")
def list_installed_applications():
    """Liste toutes les applications installées sur le périphérique."""
    logger.debug("Entrée dans la fonction list_installed_applications")
    apps = AdbApplications.list_installed()
    logger.debug(f"Applications installées: {apps}")
    return apps

@router.get("/info")
def get_application_info(package_name: str):
    """Obtient les informations d'une application spécifique."""
    logger.debug(f"Entrée dans la fonction get_application_info avec package_name={package_name}")
    info = AdbApplications.get_info(package_name)
    logger.debug(f"Informations de l'application {package_name}: {info}")
    return info

@router.post("/start")
def start_application(package_name: str):
    """Démarre une application en utilisant son nom de package."""
    logger.debug(f"Entrée dans la fonction start_application avec package_name={package_name}")
    result = AdbApplications.start(package_name)
    logger.debug(f"Résultat du démarrage: {result}")
    return result

@router.post("/stop")
def stop_application(package_name: str):
    """Arrête une application en utilisant son nom de package."""
    logger.debug(f"Entrée dans la fonction stop_application avec package_name={package_name}")
    result = AdbApplications.stop(package_name)
    logger.debug(f"Résultat de l'arrêt: {result}")
    return result

@router.get("/is_running")
def is_application_running(package_name: str):
    """Vérifie si une application est en cours d'exécution."""
    logger.debug(f"Entrée dans la fonction is_application_running avec package_name={package_name}")
    result = AdbApplications.is_running(package_name)
    logger.debug(f"Résultat de la vérification: {result}")
    return result