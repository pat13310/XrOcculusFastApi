from fastapi import APIRouter, HTTPException
from adb.adb_services_files import AdbFiles
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
def list_files(path: str = "/sdcard"):
    """Liste les fichiers dans un répertoire donné."""
    logger.debug(f"Entrée dans la fonction list_files avec path={path}")
    try:
        files = AdbFiles.list_files(path)
        logger.debug(f"Fichiers listés: {files}")
        return {"files": files}
    except Exception as e:
        logger.error(f"Erreur lors de la liste des fichiers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pull")
def pull_file(source: str, destination: str):
    """Copie un fichier du périphérique vers le système local."""
    logger.debug(f"Entrée dans la fonction pull_file avec source={source}, destination={destination}")
    try:
        result = AdbFiles.pull(source, destination)
        logger.debug(f"Résultat du pull: {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Erreur lors du pull du fichier: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/push")
def push_file(source: str, destination: str):
    """Copie un fichier du système local vers le périphérique."""
    logger.debug(f"Entrée dans la fonction push_file avec source={source}, destination={destination}")
    try:
        result = AdbFiles.push(source, destination)
        logger.debug(f"Résultat du push: {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Erreur lors du push du fichier: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
def delete_file(path: str):
    """Supprime un fichier sur le périphérique."""
    logger.debug(f"Entrée dans la fonction delete_file avec path={path}")
    try:
        result = AdbFiles.delete_file(path)
        logger.debug(f"Résultat de la suppression: {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du fichier: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/details")
def file_details(path: str):
    """Obtient les détails d'un fichier sur le périphérique."""
    logger.debug(f"Entrée dans la fonction file_details avec path={path}")
    try:
        details = AdbFiles.file_details(path)
        logger.debug(f"Détails du fichier: {details}")
        return details
    except Exception as e:
        logger.error(f"Erreur lors de l'obtention des détails du fichier: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mkdir")
def create_directory(path: str):
    """Crée un répertoire sur le périphérique."""
    logger.debug(f"Entrée dans la fonction create_directory avec path={path}")
    try:
        result = AdbFiles.create_directory(path)
        logger.debug(f"Résultat de la création du répertoire: {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Erreur lors de la création du répertoire: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chmod")
def change_permissions(path: str, permissions: str):
    """Change les permissions d'un fichier sur le périphérique."""
    logger.debug(f"Entrée dans la fonction change_permissions avec path={path}, permissions={permissions}")
    try:
        result = AdbFiles.change_permissions(path, permissions)
        logger.debug(f"Résultat du changement de permissions: {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Erreur lors du changement de permissions: {e}")
        raise HTTPException(status_code=500, detail=str(e))