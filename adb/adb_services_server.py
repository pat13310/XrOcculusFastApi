from adb.adb_command_executor import AdbCommandExecutor
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AdbServer:
    _server_process = None

    @classmethod
    def start_server(cls) -> Dict[str, str]:
        try:
            AdbCommandExecutor.execute(["start-server"])
            return {"statut": "Succès", "message": "Serveur ADB démarré"}
        except Exception as e:
            logger.error(f"Erreur lors du démarrage du serveur ADB : {str(e)}")
            return {"statut": "Erreur", "message": str(e)}

    @classmethod
    def stop_server(cls) -> Dict[str, str]:
        try:
            AdbCommandExecutor.execute(["kill-server"])
            return {"statut": "Succès", "message": "Serveur ADB arrêté"}
        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt du serveur ADB : {str(e)}")
            return {"statut": "Erreur", "message": str(e)}

    @classmethod
    def restart_server(cls) -> Dict[str, str]:
        try:
            cls.stop_server()
            cls.start_server()
            return {"statut": "Succès", "message": "Serveur ADB redémarré"}
        except Exception as e:
            logger.error(f"Erreur lors du redémarrage du serveur ADB : {str(e)}")
            return {"statut": "Erreur", "message": str(e)}

    @classmethod
    def server_status(cls) -> str:
        try:
            output = AdbCommandExecutor.execute(["version"])
            return f"Serveur ADB actif : {output}"
        except Exception as e:
            logger.warning(f"Statut du serveur ADB inconnu : {str(e)}")
            return "Serveur ADB inactif"
