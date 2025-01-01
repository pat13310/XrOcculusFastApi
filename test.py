import subprocess
import shutil
import logging
import re
from enum import Enum, auto
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)

try:
    import psutil
    PSUTIL_DISPONIBLE = True
except ImportError:
    PSUTIL_DISPONIBLE = False


class AdbServiceCategory(Enum):
    PERIPHERIQUE = auto()
    RESEAU = auto()
    SYSTEME = auto()
    APPLICATION = auto()
    FICHIERS = auto()


class AdbCommandExecutor:
    @staticmethod
    def execute(command: List[str], handle_errors: bool = True) -> str:
        if not shutil.which("adb"):
            raise RuntimeError("ADB n'est pas installé ou introuvable dans le PATH")
        try:
            result = subprocess.run(
                ["adb"] + command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            if handle_errors:
                return f"Erreur : {e.stderr}"
            raise RuntimeError(f"Échec de la commande ADB : {e.stderr}")


class AdbSystem:
    @staticmethod
    def get_android_version() -> str:
        return AdbCommandExecutor.execute(["shell", "getprop", "ro.build.version.release"])

    @staticmethod
    def reboot() -> str:
        return AdbCommandExecutor.execute(["reboot"])

    @staticmethod
    def shutdown() -> str:
        return AdbCommandExecutor.execute(["shell", "reboot", "-p"])

    @staticmethod
    def battery_info() -> Dict[str, Any]:
        output = AdbCommandExecutor.execute(["shell", "dumpsys", "battery"])
        info = {
            line.split(': ')[0].strip(): line.split(': ')[1].strip()
            for line in output.splitlines()
            if ': ' in line
        }
        return {
            'niveau': info.get('level', 'N/A'),
            'statut': info.get('status', 'N/A'),
            'temperature': float(info.get('temperature', 0)) / 10 if 'temperature' in info else 'N/A',
            'technologie': info.get('technology', 'N/A'),
            'voltage': info.get('voltage', 'N/A')
        }

    @staticmethod
    def uptime() -> str:
        return AdbCommandExecutor.execute(["shell", "uptime"])

    @staticmethod
    def screen_status() -> str:
        output = AdbCommandExecutor.execute(["shell", "dumpsys", "power"])
        match = re.search(r'mScreenOn=(true|false)', output)
        return "On" if match and match.group(1) == "true" else "Off"

    @staticmethod
    def thermal_info() -> Dict[str, str]:
        output = AdbCommandExecutor.execute(["shell", "dumpsys", "thermalservice"])
        return {
            line.split(': ')[0].strip(): line.split(': ')[1].strip()
            for line in output.splitlines()
            if ': ' in line
        }

    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        output = AdbCommandExecutor.execute(["shell", "cat", "/proc/cpuinfo"])
        return {
            line.split(':')[0].strip(): line.split(':')[1].strip()
            for line in output.splitlines()
            if ':' in line
        }

    @staticmethod
    def memory_info() -> Dict[str, Any]:
        output = AdbCommandExecutor.execute(["shell", "cat", "/proc/meminfo"])
        return {
            line.split(':')[0].strip(): line.split(':')[1].strip()
            for line in output.splitlines()
            if ':' in line
        }

    @staticmethod
    def date_time() -> str:
        return AdbCommandExecutor.execute(["shell", "date"])

    @staticmethod
    def device_model() -> str:
        return AdbCommandExecutor.execute(["shell", "getprop", "ro.product.model"])

    @staticmethod
    def device_manufacturer() -> str:
        return AdbCommandExecutor.execute(["shell", "getprop", "ro.product.manufacturer"])


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
