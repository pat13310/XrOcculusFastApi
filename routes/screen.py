import subprocess
from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from adb.adb_command_executor import AdbCommandExecutor

router = APIRouter()

class Screen(BaseModel):
    path: str
    duration: int = 10  # Durée maximale en secondes (par défaut 10 secondes)
    prefix:str="video"
@router.post("/screen/video/capture")
async def start_screen_capture(screen: Screen):
    """Démarre la capture vidéo de l'écran."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path_with_timestamp = f"{screen.path}{screen.prefix}_{timestamp}.mp4"
        
        command = [
            "shell", "screenrecord", "--time-limit", str(screen.duration), path_with_timestamp
        ]

        # Exécuter la commande adb
        result = AdbCommandExecutor.execute(command)

        # Vérifiez si la commande a échoué en raison de la résolution
        if "unable to configure video/avc codec" in result:
            # Réessayez avec une résolution plus basse
            command = [
                "shell", "screenrecord", "--size", "720x1280", "--time-limit", str(screen.duration), path_with_timestamp
            ]
            result = AdbCommandExecutor.execute(command)

        return {
            "status": "success",
            "message": "Capture vidéo démarrée avec succès",
            "details": {
                "path": path_with_timestamp,
                "result": result
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du démarrage de la capture vidéo: {str(e)}"
        )

@router.post("/screen/video/stop")
async def stop_screen_capture():
    """Arrête la capture vidéo de l'écran."""
    try:
        command = [
            "shell", "killall", "screenrecord"
        ]

        # Exécuter la commande adb
        result = AdbCommandExecutor.execute(command)

        return {
            "status": "success",
            "message": "Capture vidéo arrêtée avec succès",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'arrêt de la capture vidéo: {str(e)}"
        )

class ImageCapture(BaseModel):
    path: str
    prefix:str="image"

@router.post("/screen/image/capture")
async def capture_image(screen: ImageCapture):
    """Capture une image de l'écran."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path_with_timestamp = f"{screen.path}{screen.prefix}_{timestamp}.png"
        
        command = [
            "shell", "screencap", path_with_timestamp
        ]

        # Exécuter la commande adb
        result = AdbCommandExecutor.execute(command)

        return {
            "status": "success",
            "message": "Capture d'image réussie",
            "details": {
                "path": path_with_timestamp,
                "result": result
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la capture d'image: {str(e)}"
        )
    
def video_stream_generator():
    process = subprocess.Popen(
        ["adb", "shell", "screenrecord", "--output-format=h264", "-"],
        stdout=subprocess.PIPE
    )
    while True:
        chunk = process.stdout.read(1024)
        if not chunk:
            break
        yield chunk

@router.post("/screen/video/stream")
async def stream_video():
    return StreamingResponse(video_stream_generator(), media_type="video/mp4")
