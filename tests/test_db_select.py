import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Initialiser le client Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Créer la table via l'API Supabase
try:
    # Essayer de sélectionner depuis la table
    try:
        supabase.table("test").select("*").limit(1).execute()
        print("La table 'test' existe déjà")
    except Exception:
        # Créer la table si elle n'existe pas
        supabase.from_("sql").insert({
            "query": """
                CREATE TABLE test (
                    id SERIAL PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL
                );
            """
        }).execute()
        print("Table 'test' créée avec succès")
except Exception as e:
    print(f"Erreur lors de la création de la table : {str(e)}")
    exit(1)

# Vérifier si l'enregistrement existe déjà
existing = supabase.table("test").select("name").eq("name", "Anya").execute()

if not existing.data:
    # Insérer seulement si le nom n'existe pas
    try:
        supabase.table("test").insert({ "name": "Anya"}).execute()
        print("Nouvel enregistrement inséré")
    except Exception as e:
        print(f"Erreur lors de l'insertion : {str(e)}")
else:
    print("L'enregistrement existe déjà")

# Récupérer tous les enregistrements
result = supabase.table("test").select("*").execute()
print("Tous les enregistrements :")
print(result.data)
