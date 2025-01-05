from adb.adb_command_executor import AdbCommandExecutor
from typing import List, Dict, Any
import logging
import re

logger = logging.getLogger(__name__)

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
