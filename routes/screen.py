import subprocess
from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import time
import threading

from adb.adb_command_executor import AdbCommandExecutor

router = APIRouter()

# État global pour le streaming
stop_stream = False

### 📹 **1. Capture Vidéo (Enregistrement)**
class Screen(BaseModel):
    path: str
    duration: int = 10  # Durée maximale en secondes (par défaut 10 secondes)
    prefix: str = "video"
    resolution: str = "1280x720"


@router.post("/screen/video/capture")
async def start_screen_capture(screen: Screen):
    """Démarre la capture vidéo de l'écran."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path_with_timestamp = f"{screen.path}_{timestamp}.mp4"
        
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
### 🖼️ **2. Capture d'Image (Screenshot)**

class ImageCapture(BaseModel):
    path: str
    prefix: str = "image"


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


### 🎥 **3. Streaming Vidéo en Temps Réel**

stream_thread = None


def adb_screen_stream():
    """
    Capture et diffuse les captures d'écran Android en continu via ADB.
    """
    global stop_stream
    try:
        while not stop_stream:
            process = subprocess.Popen(
                ["adb", "exec-out", "screencap", "-p"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            image_data = process.stdout.read()
            if not image_data:
                continue  # Ignore les images invalides

            yield (b'--frame\r\n' b'Content-Type: image/png\r\n\r\n' + image_data + b'\r\n')
            
            time.sleep(0.5)  # Ajuster le délai pour le framerate

    except Exception as e:
        print(f"❌ Erreur dans le flux : {e}")
    finally:
        print("🔴 Flux de capture arrêté proprement.")

def adb_screen_stream_opencv():
    """
    Diffuse le flux vidéo Android avec OpenCV et ADB via `screencap`.
    """
    global stop_stream
    try:
        while not stop_stream:
            # Capture via ADB
            process = subprocess.Popen(
                ["adb", "exec-out", "screencap", "-p"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            image_data = process.stdout.read()
            if not image_data:
                continue  # Ignore les données invalides

            # Décodage avec OpenCV
            img_array = np.frombuffer(image_data, dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if frame is None:
                continue

            # Redimensionner pour des performances accrues
            frame = cv2.resize(frame, (640, 480))

            # Compression en JPEG pour un transfert efficace
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])

            # Envoi du flux MJPEG
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

            time.sleep(0.03)  # Contrôle du framerate (~30 FPS)

    except Exception as e:
        print(f"❌ Erreur du flux : {e}")
    finally:
        print("🔴 Flux arrêté proprement.")


### ▶️ **1. Démarrer le Streaming d'Écran**
@router.post("/screen/video/stream/start")
async def start_stream():
    """
    Démarre la capture continue de l'écran Android.
    """
    global stop_stream, stream_thread
    stop_stream = False

    if stream_thread is None or not stream_thread.is_alive():
        stream_thread = threading.Thread(target=adb_screen_stream)
        stream_thread.start()

    return JSONResponse(
        content={"status": "success", "message": "Streaming démarré."},
        headers={"Access-Control-Allow-Origin": "*"}
    )


### ⏹️ **2. Arrêter le Streaming d'Écran**
@router.post("/screen/video/stream/stop")
async def stop_streaming():
    """
    Arrête la capture continue de l'écran Android.
    """
    global stop_stream
    stop_stream = True

    return JSONResponse(
        content={"status": "success", "message": "Streaming arrêté."},
        headers={"Access-Control-Allow-Origin": "*"}
    )


### 📺 **3. Diffuser le Flux d'Écran**
@router.get("/screen/video/stream")
async def stream_screen():
    """
    Diffuse en continu les captures d'écran Android via ADB.
    """
    global stop_stream
    if stop_stream:
        raise HTTPException(status_code=400, detail="Le streaming n'est pas démarré. Lancez `/screen/start` d'abord.")

    return StreamingResponse(
        adb_screen_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@router.get("/screen/video/stream2")
async def stream_screen():
    """
    Démarre le streaming vidéo depuis Android avec OpenCV et FastAPI.
    """
    global stop_stream
    stop_stream = False
    return StreamingResponse(
        adb_screen_stream_opencv(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
