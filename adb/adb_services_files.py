from adb.adb_command_executor import AdbCommandExecutor
from typing import List, Dict, Any
import logging


logger = logging.getLogger(__name__)


class AdbFiles:
    @staticmethod
    def list_files(path: str = "/sdcard") -> List[str]:
        output = AdbCommandExecutor.execute(["shell", "ls", path])
        return output.splitlines()

    @staticmethod
    def pull(source: str, destination: str) -> str:
        return AdbCommandExecutor.execute(["pull", source, destination])

    @staticmethod
    def push(source: str, destination: str) -> str:
        return AdbCommandExecutor.execute(["push", source, destination])

    @staticmethod
    def delete_file(path: str) -> str:
        return AdbCommandExecutor.execute(["shell", "rm", path])

    @staticmethod
    def file_details(path: str) -> Dict[str, str]:
        output = AdbCommandExecutor.execute(["shell", "ls", "-l", path])
        return {"details": output}

    @staticmethod
    def create_directory(path: str) -> str:
        return AdbCommandExecutor.execute(["shell", "mkdir", "-p", path])

    @staticmethod
    def change_permissions(path: str, permissions: str) -> str:
        return AdbCommandExecutor.execute(["shell", "chmod", permissions, path])

    @staticmethod
    def search_files(path: str, pattern: str) -> List[str]:
        output = AdbCommandExecutor.execute(["shell", "find", path, "-name", pattern])
        return output.splitlines()

    @staticmethod
    def move_file(source: str, destination: str) -> str:
        return AdbCommandExecutor.execute(["shell", "mv", source, destination])

    @staticmethod
    def copy_file(source: str, destination: str) -> str:
        return AdbCommandExecutor.execute(["shell", "cp", source, destination])

    @staticmethod
    def file_size(path: str) -> str:
        output = AdbCommandExecutor.execute(["shell", "stat", "-c", "%s", path])
        return f"{output} bytes"

    @staticmethod
    def file_type(path: str) -> str:
        return AdbCommandExecutor.execute(["shell", "file", path])

    @staticmethod
    def check_file_exists(path: str) -> bool:
        output = AdbCommandExecutor.execute(["shell", "test", "-e", path, "&&", "echo", "exists"])
        return output.strip() == "exists"

    @staticmethod
    def read_file(path: str) -> str:
        return AdbCommandExecutor.execute(["shell", "cat", path])

    @staticmethod
    def write_to_file(path: str, content: str) -> str:
        return AdbCommandExecutor.execute(["shell", "echo", f"{content}", ">", path])

    @staticmethod
    def tail_file(path: str, lines: int = 10) -> str:
        return AdbCommandExecutor.execute(["shell", "tail", f"-n {lines}", path])

    @staticmethod
    def head_file(path: str, lines: int = 10) -> str:
        return AdbCommandExecutor.execute(["shell", "head", f"-n {lines}", path])

    @staticmethod
    def zip_directory(source: str, destination: str) -> str:
        return AdbCommandExecutor.execute(["shell", "zip", "-r", destination, source])

    @staticmethod
    def unzip_file(source: str, destination: str) -> str:
        return AdbCommandExecutor.execute(["shell", "unzip", source, "-d", destination])

    @staticmethod
    def disk_usage(path: str) -> str:
        return AdbCommandExecutor.execute(["shell", "du", "-sh", path])

    @staticmethod
    def list_open_files() -> List[str]:
        output = AdbCommandExecutor.execute(["shell", "lsof"])
        return output.splitlines()

    @staticmethod
    def sync_files() -> str:
        return AdbCommandExecutor.execute(["sync"])

    @staticmethod
    def get_file_checksum(path: str) -> str:
        return AdbCommandExecutor.execute(["shell", "md5sum", path])

    @staticmethod
    def create_symlink(source: str, destination: str) -> str:
        return AdbCommandExecutor.execute(["shell", "ln", "-s", source, destination])

    @staticmethod
    def list_directory_detailed(path: str) -> str:
        return AdbCommandExecutor.execute(["shell", "ls", "-alh", path])

    @staticmethod
    def truncate_file(path: str, size: int) -> str:
        return AdbCommandExecutor.execute(["shell", "truncate", f"-s {size}", path])

    @staticmethod
    def rename_file(old_name: str, new_name: str) -> str:
        return AdbCommandExecutor.execute(["shell", "mv", old_name, new_name])

    @staticmethod
    def count_files(path: str) -> str:
        return AdbCommandExecutor.execute(["shell", "find", path, "-type", "f", "|", "wc", "-l"])
