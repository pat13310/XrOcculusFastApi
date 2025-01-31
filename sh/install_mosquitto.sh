#!/bin/bash

# Vérifier si l'utilisateur est root
if [ "$(id -u)" -ne 0 ]; then
    echo "Ce script doit être exécuté en tant que root (utilisez sudo)." >&2
    exit 1
fi

echo "Mise à jour du système..."
apt update && apt upgrade -y

echo "Installation de Mosquitto et des clients MQTT..."
apt install -y mosquitto mosquitto-clients

echo "Configuration de Mosquitto pour autoriser les connexions externes..."
cat > /etc/mosquitto/mosquitto.conf <<EOF
listener 1883
allow_anonymous true
EOF

echo "Redémarrage du service Mosquitto..."
systemctl restart mosquitto
systemctl enable mosquitto

echo "Ouverture du port 1883 dans le pare-feu..."
ufw allow 1883/tcp
ufw enable

echo "Installation terminée avec succès !"
echo "Le serveur MQTT Mosquitto est maintenant opérationnel sur le port 1883."

read -p "Voulez-vous activer l'authentification par mot de passe ? (o/n) " choix
if [[ "$choix" =~ ^[Oo]$ ]]; then
    read -p "Entrez le nom d'utilisateur MQTT : " mqtt_user
    mosquitto_passwd -c /etc/mosquitto/passwd "$mqtt_user"
    
    echo "Mise à jour de la configuration pour sécuriser Mosquitto..."
    cat > /etc/mosquitto/mosquitto.conf <<EOF
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
EOF

    echo "Redémarrage de Mosquitto avec authentification..."
    systemctl restart mosquitto
    echo "Sécurité activée ! Vous devez maintenant vous connecter avec un identifiant/mot de passe."
fi

echo "Installation et configuration terminées ! 🚀"
