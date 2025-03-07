import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")  # Utiliser la clé de rôle de service

# Vérifier que les configurations sont chargées
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE:
    raise ValueError("Les variables d'environnement SUPABASE_URL ou SUPABASE_SERVICE_ROLE ne sont pas définies.")

# Créer un client Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

# Ajouter un utilisateur
def signup_user(email: str, password: str):
    try:
        # Appeler la méthode de création d'utilisateur
        response = supabase.auth.sign_up({"email": email, "password": password})
        print("User created successfully:", response)
        return response
    except Exception as e:
        print("Error during signup:", e)
        return None

# Exemple d'appel
if __name__ == "__main__":
    email = "demo2@example.com"  # Remplacez par une adresse e-mail valide
    password = "demo123"  # Remplacez par un mot de passe sécurisé
    new_user = signup_user(email, password)
