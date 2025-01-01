from adb.adb_command_executor import AdbCommandExecutor
from typing import List, Dict, Any
import logging
import re

logger = logging.getLogger(__name__)


class AdbNetwork:
    @staticmethod
    def toggle_wifi(enable: bool) -> Dict[str, Any]:
        """Active ou désactive le WiFi."""
        state = "enable" if enable else "disable"
        return AdbCommandExecutor.execute(["shell", f"svc wifi {state}"])

    @staticmethod
    def wifi_status() -> Dict[str, Any]:
        """Récupère l'état actuel du WiFi."""
        return AdbCommandExecutor.execute(["shell", "dumpsys", "wifi"])

    @staticmethod
    def get_connected_ssid() -> Dict[str, Any]:
        """Récupère le SSID du réseau WiFi connecté."""
        output = AdbCommandExecutor.execute(["shell", "dumpsys", "wifi", "|", "grep", "SSID"])
        if output.get("statut") == "Succès":
            match = re.search(r'SSID: (.+)', output.get("sortie", ""))
            return {
                "statut": "Succès",
                "SSID": match.group(1).strip() if match else "SSID non disponible"
            }
        return output

    @staticmethod
    def get_wifi_ip() -> Dict[str, Any]:
        """Récupère l'adresse IP du WiFi."""
        output = AdbCommandExecutor.execute(["shell", "ifconfig", "wlan0"])
        if output.get("statut") == "Succès":
            match = re.search(r'inet addr:(\d+\.\d+\.\d+\.\d+)', output.get("sortie", ""))
            return {
                "statut": "Succès",
                "adresse_ip": match.group(1) if match else "Adresse IP non disponible"
            }
        return output

    @staticmethod
    def reset_wifi() -> Dict[str, Any]:
        """Réinitialise le WiFi."""
        return AdbCommandExecutor.execute(["shell", "svc wifi disable && svc wifi enable"])

    @staticmethod
    def wifi_signal_strength() -> Dict[str, Any]:
        """Récupère la force du signal WiFi."""
        output = AdbCommandExecutor.execute(["shell", "dumpsys", "wifi", "|", "grep", "RSSI"])
        if output.get("statut") == "Succès":
            match = re.search(r'RSSI: (-?\d+)', output.get("sortie", ""))
            return {
                "statut": "Succès",
                "force_signal": match.group(1) if match else "Force du signal non disponible"
            }
        return output

    @staticmethod
    def wifi_frequency() -> Dict[str, Any]:
        """Récupère la fréquence du réseau WiFi actuel."""
        output = AdbCommandExecutor.execute(["shell", "dumpsys", "wifi", "|", "grep", "Frequency"])
        if output.get("statut") == "Succès":
            match = re.search(r'Frequency: (\d+)', output.get("sortie", ""))
            return {
                "statut": "Succès",
                "frequence": match.group(1) if match else "Fréquence non disponible"
            }
        return output
