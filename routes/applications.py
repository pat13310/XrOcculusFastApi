from fastapi import APIRouter, HTTPException, Request
from adb.adb_services_applications import AdbApplications
import os
import logging
from decorators import jwt_required

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/app/install")
@jwt_required
async def install_application(request:Request, apk_path: str):
    """Installe une application à partir d'un fichier APK."""
    logger.debug(f"Entrée dans la fonction install_application avec apk_path={apk_path}")
    if not os.path.isfile(apk_path) or not apk_path.endswith('.apk'):
        logger.warning(f"Chemin APK invalide: {apk_path}")
        raise HTTPException(status_code=400, detail=f"Le chemin APK '{apk_path}' est invalide ou le fichier n'existe pas.")
    result = AdbApplications.install(apk_path)
    logger.debug(f"Résultat de l'installation: {result}")
    return result

@router.post("/app/uninstall")
@jwt_required
async def uninstall_application(request:Request,package_name: str):
    """Désinstalle une application en utilisant son nom de package."""
    logger.debug(f"Entrée dans la fonction uninstall_application avec package_name={package_name}")
    result = AdbApplications.uninstall(package_name)
    logger.debug(f"Résultat de la désinstallation: {result}")
    return result

@router.get("/app/list/shop")
@jwt_required
async def list_applications(request:Request):
    """Liste toutes les applications installées et non installées dans la boutique."""
    logger.debug("Entrée dans la fonction list_installed_applications")
    apps = AdbApplications.list_installed()
    logger.debug(f"Applications installées: {apps}")
    return apps

@router.get("/app/list/used")
@jwt_required
async def list_used_applications(request:Request):
    """
    Liste toutes les applications utilisées sur le périphérique, 
    incluant les applications système.
    """
    logger.debug("Entrée dans la fonction list_used_applications")
    apps = AdbApplications.list_installed()
    logger.debug(f"Applications installées: {apps}")
    return apps

@router.get("/app/list/uninstalled")
@jwt_required
async def list_uninstalled_applications(request:Request):
    """Liste toutes les applications disponibles(non installées)  sur le périphérique."""
    logger.debug("Entrée dans la fonction list_installed_applications")
    apps = AdbApplications.list_installed()
    logger.debug(f"Applications installées: {apps}")
    return apps


@router.get("/app/info")
@jwt_required
async def get_application_info(request:Request,package_name: str):
    """Obtient les informations d'une application spécifique."""
    logger.debug(f"Entrée dans la fonction get_application_info avec package_name={package_name}")
    info = AdbApplications.get_info(package_name)
    logger.debug(f"Informations de l'application {package_name}: {info}")
    return info

@router.post("/app/start")
@jwt_required
async def start_application(request:Request,package_name: str):
    """Démarre une application en utilisant son nom de package."""
    logger.debug(f"Entrée dans la fonction start_application avec package_name={package_name}")
    result = AdbApplications.start(package_name)
    logger.debug(f"Résultat du démarrage: {result}")
    return result

@router.post("/app/stop")
@jwt_required
async def stop_application(request:Request,package_name: str):
    """Arrête une application en utilisant son nom de package."""
    logger.debug(f"Entrée dans la fonction stop_application avec package_name={package_name}")
    result = AdbApplications.stop(package_name)
    logger.debug(f"Résultat de l'arrêt: {result}")
    return result

@router.get("/app/is_running")
@jwt_required
async def is_application_running(request:Request,package_name: str):
    """Vérifie si une application est en cours d'exécution."""
    logger.debug(f"Entrée dans la fonction is_application_running avec package_name={package_name}")
    result = AdbApplications.is_running(package_name)
    logger.debug(f"Résultat de la vérification: {result}")
    return result