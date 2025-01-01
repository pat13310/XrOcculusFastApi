from typing import List, Dict, Any
from adb.adb_command_executor import AdbCommandExecutor
import logging


logger = logging.getLogger(__name__)


class AdbApplications:
    @staticmethod
    def list_installed_apps() -> Dict[str, Any]:
        """Liste toutes les applications installées sur l'appareil Android."""
        output = AdbCommandExecutor.execute(["shell", "pm", "list", "packages"])
        if output.get("statut") == "Succès":
            apps = [line.split(":")[1] for line in output.get("sortie", "").splitlines()]
            return {"statut": "Succès", "applications": apps}
        return output

    @staticmethod
    def install_app(apk_path: str) -> Dict[str, Any]:
        """Installe une application via un fichier APK."""
        return AdbCommandExecutor.execute(["install", apk_path])

    @staticmethod
    def uninstall_app(package_name: str) -> Dict[str, Any]:
        """Désinstalle une application."""
        return AdbCommandExecutor.execute(["uninstall", package_name])

    @staticmethod
    def clear_app_data(package_name: str) -> Dict[str, Any]:
        """Efface les données d'une application spécifique."""
        return AdbCommandExecutor.execute(["shell", "pm", "clear", package_name])

    @staticmethod
    def start_app(package_name: str, activity: str) -> Dict[str, Any]:
        """Démarre une application spécifique."""
        return AdbCommandExecutor.execute(["shell", "am", "start", "-n", f"{package_name}/{activity}"])

    @staticmethod
    def stop_app(package_name: str) -> Dict[str, Any]:
        """Arrête une application spécifique."""
        return AdbCommandExecutor.execute(["shell", "am", "force-stop", package_name])
