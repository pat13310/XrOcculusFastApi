import requests

def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        ip = response.json()["ip"]
        return ip
    except requests.RequestException as e:
        return f"Erreur : {e}"



def get_public_ipv4():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        ip = response.json()["ip"]
        return ip
    except requests.RequestException as e:
        return f"Erreur : {e}"

# Test
print("Adresse IP publique IPv4 :", get_public_ipv4())

# Test
print("Adresse IP publique :", get_public_ip())
