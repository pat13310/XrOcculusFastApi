import os
import platform
import subprocess
import zipfile
import shutil

def download_adb():
    system = platform.system()
    urls = {
        "Linux": "https://dl.google.com/android/repository/platform-tools-latest-linux.zip",
        "Darwin": "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip",
        "Windows": "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
    }

    if system not in urls:
        print("Système d'exploitation non pris en charge.")
        return False

    url = urls[system]
    zip_file = "platform-tools.zip"

    print(f"📥 Téléchargement d'ADB pour {system} depuis : {url}")
    subprocess.run(["wget", url, "-O", zip_file], check=True)

    return zip_file

def extract_zip(zip_file, destination):
    print(f"📦 Extraction de {zip_file} vers {destination}")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination)
    os.remove(zip_file)

def add_to_path(destination):
    system = platform.system()
    adb_path = os.path.abspath(destination)

    if system == "Windows":
        path_cmd = f'setx PATH "%PATH%;{adb_path}"'
        subprocess.run(path_cmd, shell=True)
        print("✅ PATH mis à jour sur Windows.")
    else:
        shell_rc = os.path.expanduser("~/.bashrc") if system == "Linux" else os.path.expanduser("~/.zshrc")
        with open(shell_rc, "a") as file:
            file.write(f'\nexport PATH=$PATH:{adb_path}\n')
        subprocess.run(["source", shell_rc], shell=True)
        print(f"✅ PATH mis à jour dans {shell_rc}.")

def verify_adb():
    try:
        result = subprocess.run(["adb", "version"], capture_output=True, text=True, check=True)
        print("✅ ADB installé avec succès :", result.stdout)
    except subprocess.CalledProcessError:
        print("❌ Erreur : ADB n'est pas correctement installé.")

def main():
    print("🚀 Début de l'installation automatique d'ADB")
    home_dir = os.path.expanduser("~")
    adb_dir = os.path.join(home_dir, "platform-tools")

    try:
        zip_file = download_adb()
        extract_zip(zip_file, adb_dir)
        add_to_path(adb_dir)
        verify_adb()
        print("🎉 Installation d'ADB terminée avec succès !")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution : {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")

if __name__ == "__main__":
    main()
