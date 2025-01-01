import subprocess
import shutil
from typing import List, Dict, Any
from enum import Enum, auto

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