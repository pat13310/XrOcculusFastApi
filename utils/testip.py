import socket

def recuperer_ip_locale() -> str:
    """
    Récupère l'adresse IP locale de la machine.
    On utilise une connexion UDP vers une adresse IP fictive pour obtenir l'IP de sortie.
    En cas d'erreur, retourne '127.0.0.1'.
    
    :return: Adresse IP locale sous forme de chaîne de caractères.
    """
    try:
        # Création d'une socket UDP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # La connexion n'envoie pas de données réelles mais permet d'obtenir l'IP locale
            s.connect(('10.255.255.255', 1))
            ip_locale = s.getsockname()[0]
    except Exception as e:
        # En cas d'erreur, on retourne l'IP localhost
        print(f"Erreur lors de la récupération de l'IP locale : {e}")
        ip_locale = '127.0.0.1'
    return ip_locale

if __name__ == "__main__":
    ip = recuperer_ip_locale()
    print(f"L'adresse IP locale est : {ip}")
