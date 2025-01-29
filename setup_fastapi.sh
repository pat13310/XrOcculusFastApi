#!/bin/bash

# Arrêter le script en cas d'erreur
set -e

echo "🚀 Début de l'installation de XrOcculusFastAPI..."

# ✅ Définition du dossier de l'application
APP_DIR="/root/server/XrOcculusFastAPI"

# ✅ Cloner ou mettre à jour le dépôt GitHub
if [ -d "$APP_DIR" ]; then
    echo "🔄 Mise à jour du projet existant..."
    cd $APP_DIR
    git pull origin main
else
    echo "📂 Clonage du dépôt GitHub..."
    mkdir -p /server
    git clone https://github.com/pat13310/XrOcculusFastApi.git $APP_DIR
    cd $APP_DIR
fi

# ✅ Créer et activer l'environnement virtuel
echo "🌍 Configuration de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

# ✅ Installer les dépendances
echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# ✅ Vérifier que l'application est bien installée
echo "✅ Installation terminée !"

# ✅ Relancer l'application avec Uvicorn (optionnel)
#echo "🚀 Démarrage de l'application..."
#nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &

#echo "🎉 XrOcculusFastAPI est maintenant en cours d'exécution !"

