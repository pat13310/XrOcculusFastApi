from adb.adb_command_executor import AdbCommandExecutor
from typing import List, Dict, Any
import logging
import re

logger = logging.getLogger(__name__)

class AdbSystem:
    @staticmethod
    def parse_output(output: str) -> Dict[str, Any]:
        """Transforme la sortie brute en JSON structuré."""
        parsed_data = {}
        for line in output.splitlines():
            if ": " in line:
                key, value = line.split(": ", 1)
                parsed_data[key.strip()] = value.strip()
        return parsed_data

    @staticmethod
    def parse_uptime(output: str) -> Dict[str, Any]:
        """Transforme la sortie brute de la commande uptime en JSON structuré."""
        match = re.match(r"(\d+:\d+:\d+) up (.*),\s+(\d+) users?,\s+load average: (.*)", output)
        if match:
            return {
                "time": match.group(1),
                "uptime": match.group(2),
                "users": int(match.group(3)),
                "load_average": match.group(4).split(", ")
            }
        return {}

    @staticmethod
    def parse_thermal_info(output: str) -> Dict[str, Any]:
        """Transforme la sortie brute des informations thermiques en JSON structuré."""
        thermal_info = {}
        temperatures = []
        for line in output.splitlines():
            if "Temperature{" in line:
                temp_match = re.match(r"\tTemperature\{mValue=(.*?), mType=(.*?), mName=(.*?), mStatus=(.*?)\}", line)
                if temp_match:
                    temperatures.append({
                        "name": temp_match.group(3),
                        "value": float(temp_match.group(1)),
                        "type": int(temp_match.group(2)),
                        "status": int(temp_match.group(4))
                    })
            else:
                if ": " in line:
                    key, value = line.split(": ", 1)
                    thermal_info[key.strip()] = value.strip()
        thermal_info["temperatures"] = temperatures
        return thermal_info

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
        """Récupère les informations sur la batterie."""
        logger.debug("Récupération des informations sur la batterie")
        output = AdbCommandExecutor.execute(["shell", "dumpsys", "battery"])
        logger.info(f"Informations sur la batterie : {output}")
        return AdbSystem.parse_output(output)

    @staticmethod
    def uptime() -> Dict[str, Any]:
        """Récupère le temps de fonctionnement du périphérique."""
        logger.debug("Récupération du temps de fonctionnement")
        output = AdbCommandExecutor.execute(["shell", "uptime"])
        logger.info(f"Temps de fonctionnement : {output}")
        return AdbSystem.parse_uptime(output)

    @staticmethod
    def screen_status() -> str:
        """Récupère l'état de l'écran."""
        logger.debug("Récupération de l'état de l'écran")
        output = AdbCommandExecutor.execute(["shell", "dumpsys", "display"])
        logger.info(f"État de l'écran : {output}")
        return AdbSystem.parse_output(output)

    @staticmethod
    def thermal_info() -> Dict[str, Any]:
        """Récupère les informations thermiques."""
        logger.debug("Récupération des informations thermiques")
        output = AdbCommandExecutor.execute(["shell", "dumpsys", "thermalservice"])
        logger.info(f"Informations thermiques : {output}")
        return AdbSystem.parse_thermal_info(output)

    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        output = AdbCommandExecutor.execute(["shell", "cat", "/proc/cpuinfo"])
        return AdbSystem.parse_output(output)

    @staticmethod
    def memory_info() -> Dict[str, Any]:
        output = AdbCommandExecutor.execute(["shell", "cat", "/proc/meminfo"])
        return AdbSystem.parse_output(output)

    @staticmethod
    def date_time() -> str:
        return AdbCommandExecutor.execute(["shell", "date"])

    @staticmethod
    def device_model() -> str:
        return AdbCommandExecutor.execute(["shell", "getprop", "ro.product.model"])

    @staticmethod
    def device_manufacturer() -> str:
        return AdbCommandExecutor.execute(["shell", "getprop", "ro.product.manufacturer"])

    @staticmethod
    def clear_cache() -> str:
        return AdbCommandExecutor.execute(["shell", "sync; echo 3 > /proc/sys/vm/drop_caches"])

    @staticmethod
    def enable_developer_options() -> str:
        return AdbCommandExecutor.execute(["shell", "settings put global development_settings_enabled 1"])

    @staticmethod
    def disable_developer_options() -> str:
        return AdbCommandExecutor.execute(["shell", "settings put global development_settings_enabled 0"])

    @staticmethod
    def airplane_mode(enable: bool) -> str:
        state = '1' if enable else '0'
        return AdbCommandExecutor.execute(["shell", f"settings put global airplane_mode_on {state}"])

    @staticmethod
    def toggle_airplane_mode(enable: bool) -> str:
        return AdbCommandExecutor.execute(["shell", f"am broadcast -a android.intent.action.AIRPLANE_MODE --ez state {str(enable).lower()}"])

    @staticmethod
    def system_properties() -> Dict[str, str]:
        output = AdbCommandExecutor.execute(["shell", "getprop"])
        return {
            line.split(':')[0].strip('[]'): line.split(':')[1].strip('[]')
            for line in output.splitlines()
            if ':' in line
        }
