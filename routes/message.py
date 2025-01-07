from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from adb.adb_command_executor import AdbCommandExecutor

router = APIRouter()


class NotificationCmd(BaseModel):
    title: str = "Message"
    content: str
    channel_id: str = "miscellaneous"


@router.post("/notification/send")
async def send_notification_cmd(notification: NotificationCmd):
    """Envoie une notification en utilisant adb shell cmd notification post."""
    try:
        # Encadrer le contenu et le titre avec des guillemets pour éviter les problèmes d'espaces
        title_transformed = f'"{notification.title}"'
        content_transformed = f'"{notification.content}"'

        command = [
            "shell", "cmd", "notification", "post",
            "-t", title_transformed,
            "message",content_transformed,
            "--channel-id", notification.channel_id
        ]

        # Exécuter la commande adb
        result = AdbCommandExecutor.execute(command)

        return {
            "status": "success",
            "message": "Notification envoyée avec succès",
            "details": {
                "title": notification.title,
                "content": notification.content,
                "channel_id": notification.channel_id,
                "result": result
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'envoi de la notification: {str(e)}"
        )
