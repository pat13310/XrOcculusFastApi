from adb.adb_command_executor import AdbCommandExecutor
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AdbDevice:
    @staticmethod
    def list_devices() -> List[Dict[str, str]]:
        """Liste les périphériques connectés via ADB et leur état."""
        output = AdbCommandExecutor.execute(["devices"])
        devices = []
        for line in output.splitlines()[1:]:
            if 'device' in line or 'offline' in line or 'unauthorized' in line:
                parts = line.split()
                devices.append({"device": parts[0], "state": parts[1]})
        logger.info(f"Périphériques détectés : {devices}")
        return devices

    @staticmethod
    def device_info(serial: str = None) -> Dict[str, str]:
        """Récupère les informations d'un périphérique spécifique via ADB."""
        cmd = ["-s", serial, "shell", "getprop"] if serial else ["shell", "getprop"]
        output = AdbCommandExecutor.execute(cmd)
        return {
            line.split(': ')[0].strip('[]'): line.split(': ')[1].strip('[]')
            for line in output.splitlines()
            if ': ' in line
        }

    @staticmethod
    def connect(ip: str, port: int = 5555) -> Dict[str, str]:
        """Connecte un périphérique via son adresse IP et port."""
        output = AdbCommandExecutor.execute(["connect", f"{ip}:{port}"])
        if "cannot connect" not in output.lower():
            return {"statut": "Succès", "message": "Connecté", "detail": f"Périphérique {ip} connecté avec succès"}
        return {"statut": "Erreur", "message": "La connexion a échoué", "detail": output}

    @staticmethod
    def disconnect(ip: str) -> Dict[str, str]:
        """Déconnecte un périphérique spécifique par IP."""
        output = AdbCommandExecutor.execute(["disconnect", ip])
        if "disconnected" in output.lower():
            return {"statut": "Succès", "message": "Déconnecté", "detail": f"Périphérique {ip} déconnecté avec succès"}
        return {"statut": "Erreur", "message": f"La déconnexion a échoué sur {ip}"}

    @staticmethod
    def reboot(serial: str = None) -> str:
        """Redémarre un périphérique spécifique."""
        cmd = ["-s", serial, "reboot"] if serial else ["reboot"]
        return AdbCommandExecutor.execute(cmd)

    @staticmethod
    def shutdown(serial: str = None) -> str:
        """Éteint un périphérique spécifique."""
        cmd = ["-s", serial, "shell", "reboot", "-p"] if serial else ["shell", "reboot", "-p"]
        return AdbCommandExecutor.execute(cmd)

    @staticmethod
    def remount(serial: str = None) -> str:
        """Remonte le système de fichiers en mode lecture/écriture."""
        cmd = ["-s", serial, "remount"] if serial else ["remount"]
        return AdbCommandExecutor.execute(cmd)

    @staticmethod
    def get_logcat(serial: str = None) -> str:
        """Récupère les journaux du périphérique."""
        cmd = ["-s", serial, "logcat"] if serial else ["logcat"]
        return AdbCommandExecutor.execute(cmd)

    @staticmethod
    def screen_record(destination: str = "/sdcard/screenrecord.mp4", serial: str = None) -> str:
        """Enregistre l'écran du périphérique."""
        cmd = ["-s", serial, "shell", "screenrecord", destination] if serial else ["shell", "screenrecord", destination]
        return AdbCommandExecutor.execute(cmd)

    @staticmethod
    def screenshot(destination: str = "/sdcard/screenshot.png", serial: str = None) -> str:
        """Prend une capture d'écran du périphérique."""
        cmd = ["-s", serial, "shell", "screencap", "-p", destination] if serial else ["shell", "screencap", "-p", destination]
        return AdbCommandExecutor.execute(cmd)

    @staticmethod
    def install_apk(apk_path: str, serial: str = None) -> str:
        """Installe une application APK sur le périphérique."""
        cmd = ["-s", serial, "install", apk_path] if serial else ["install", apk_path]
        return AdbCommandExecutor.execute(cmd)

    @staticmethod
    def uninstall_apk(package_name: str, serial: str = None) -> str:
        """Désinstalle une application du périphérique."""
        cmd = ["-s", serial, "uninstall", package_name] if serial else ["uninstall", package_name]
        return AdbCommandExecutor.execute(cmd)

    @staticmethod
    def clear_app_data(package_name: str, serial: str = None) -> str:
        """Efface les données d'une application spécifique."""
        cmd = ["-s", serial, "shell", "pm", "clear", package_name] if serial else ["shell", "pm", "clear", package_name]
        return AdbCommandExecutor.execute(cmd)
    
    @staticmethod
    def set_mode( mode: str, port: str = "5555") -> str:
        if mode not in ["wifi", "usb"]:
            raise ValueError("Mode invalide. Utilisez 'wifi' ou 'usb'.")

        # Définition de la commande en fonction du mode choisi
        cmd = ["tcpip", port] if mode == "wifi" else ["usb"]

        # Ajouter le numéro de série si spécifié

        return AdbCommandExecutor.execute(cmd)
