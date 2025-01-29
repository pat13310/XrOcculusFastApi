#!/bin/bash

# Arrêter l'exécution en cas d'erreur
set -e

echo "🚀 Début de l'installation du serveur..."

# Mettre à jour le système
echo "🔄 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installer Python 3 et pip si ce n'est pas déjà fait
echo "🐍 Installation de Python et pip..."
sudo apt install -y python3 python3-pip

# Vérifier la version de Python installée
python3 --version
pip3 --version

# Créer le répertoire /server si inexistant
echo "📂 Création du répertoire /server..."
mkdir -p ~/server

# Vérifier si Python venv est installé et créer un environnement virtuel
echo "🌍 Configuration de l'environnement virtuel..."
sudo apt install -y python3-venv
cd ~/server
python3 -m venv venv

# Activer l'environnement virtuel
echo "✅ Activation de l'environnement virtuel..."
source venv/bin/activate

# Vérifier que tout est bien installé
echo "🔍 Vérification de l'installation..."
which python
which pip

echo "🎉 Installation terminée !"
