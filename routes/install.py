import subprocess
from fastapi import APIRouter, HTTPException
from utils import download_adb

router = APIRouter()

@router.post("/install/ffmpeg")
async def install_ffmpeg():
    """Installe FFmpeg en utilisant winget."""
    try:
        command = [
            "winget", "install", "FFmpeg (Essentials Build)"
        ]

        # Exécuter la commande winget
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        return {
            "status": "success",
            "message": "FFmpeg installé avec succès",
            "details": result.stdout.strip()
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'installation de FFmpeg: {e.stderr.strip()}"
        )
    
@router.post("/install/adb")
async def install_adb():
    """Installe ADB."""
    try:
        zip_file = download_adb()
        return {
            "status": "success",
            "message": "ADB téléchargé avec succès",
            "details": zip_file
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du téléchargement d'ADB: {str(e)}"
        )

