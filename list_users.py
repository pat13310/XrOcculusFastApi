import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")  # Utiliser la clé de rôle de service

# Créer un client Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

# Exemple : Lister les utilisateurs
def list_users():
    try:
        response = supabase.auth.admin.list_users()
        if isinstance(response, dict) and "error" in response:
            print("Erreur :", response["error"])
        else:
            print(type(response))
            if isinstance(response, list):
                print("Liste des utilisateurs :")
                for user in response:
                    print(user)
                    #print(f"Email: {user.email}, Role: {user.role}, Full Name: {user.fullname})")
    except Exception as e:
        print("Une exception s'est produite :", e)

if __name__ == "__main__":
    list_users()
