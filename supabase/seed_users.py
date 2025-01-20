from datetime import datetime
import os
import time
import datetime
from supabase import create_client
from dotenv import load_dotenv
import uuid

# Charger les variables d'environnement
load_dotenv('.env.test')

# Initialiser le client Supabase avec la clé de rôle de service
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SECRET_KEY")
)

# Données des utilisateurs
users = [
    {
        "id": str(uuid.uuid4()),
        "username": "user1",
        "email": "user1@test.com",
        "full_name": "User One",
        "password": "password1",
        "disabled": False,
        "role": "user",
        "group": None,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "deleted_at": None,
        "last_login": None
    },
    {
        "id": str(uuid.uuid4()),
        "username": "user2",
        "email": "user2@test.com",
        "full_name": "User Two",
        "password": "password2",
        "disabled": False,
        "role": "user",
        "group": None,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "deleted_at": None,
        "last_login": None
    },
    {
        "id": str(uuid.uuid4()),
        "username": "user3",
        "email": "user3@test.com",
        "full_name": "User Three",
        "password": "password3",
        "disabled": False,
        "role": "user",
        "group": None,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "deleted_at": None,
        "last_login": None
    },
    {
        "id": str(uuid.uuid4()),
        "username": "user4",
        "email": "user4@test.com",
        "full_name": "User Four",
        "password": "password4",
        "disabled": False,
        "role": "user",
        "group": None,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "deleted_at": None,
        "last_login": None
    },
    {
        "id": str(uuid.uuid4()),
        "username": "admin",
        "email": "admin@test.com",
        "full_name": "Admin User",
        "password": "admin123",
        "disabled": False,
        "role": "admin",
        "group": None,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "deleted_at": None,
        "last_login": None
    }
]

def reset_test_users():
    """Supprime et recrée les utilisateurs de test"""
    # Récupérer tous les utilisateurs existants
    existing_users = supabase.auth.admin.list_users()
    
    # Supprimer les utilisateurs de test existants
    for user in users:
        # Vérifier si l'utilisateur existe déjà
        existing_user = next((u for u in existing_users if u.email == user["email"]), None)
        if existing_user:
            try:
                # Supprimer l'utilisateur par son ID
                supabase.auth.admin.delete_user(existing_user.id)
                print(f"Utilisateur {user['email']} supprimé")
            except Exception as e:
                print(f"Erreur lors de la suppression de {user['email']}: {str(e)}")

import psycopg2

def execute_sql_file():
    """Exécute le fichier SQL pour créer les tables"""
    try:
        # Extraire les informations de connexion de l'URL Supabase
        supabase_url = os.environ.get("SUPABASE_URL")
        if not supabase_url:
            raise Exception("SUPABASE_URL non défini dans .env.test")
            
        # L'URL Supabase est au format https://project-ref.supabase.co
        # Nous devons extraire le project-ref pour construire l'URL Postgres
        project_ref = supabase_url.split('//')[1].split('.')[0]
        
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password=os.environ.get("SECRET_KEY"),
            host=f'{project_ref}.supabase.co',
            port=5432
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Lire le fichier SQL
        with open('supabase/seed.sql', 'r') as f:
            sql = f.read()
            
        # Exécuter chaque instruction SQL séparément
        for statement in sql.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
                
        cursor.close()
        conn.close()
        print("Tables créées avec succès")
        return True
    except Exception as e:
        print(f"Erreur lors de l'exécution du script SQL: {str(e)}")
        return False

def create_users():
    # Tester la connexion à Supabase
    try:
        test_response = supabase.auth.admin.list_users()
        print("Connexion à Supabase réussie")
    except Exception as e:
        print(f"Erreur de connexion à Supabase: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code}")
            print(f"Response data: {e.response.data}")
        return

    # Exécuter le script SQL pour créer les tables
    if not execute_sql_file():
        return

    # Vérifier si la table user_roles existe
    try:
        supabase.table('user_roles').select('*').limit(1).execute()
    except Exception as e:
        print("Erreur : La table user_roles n'existe pas. Veuillez exécuter le script seed.sql pour la créer.")
        return
    
    # Réinitialiser les utilisateurs de test
    reset_test_users()
    
    for user in users:
        try:
            # Créer l'utilisateur dans l'authentification
            auth_response = supabase.auth.admin.create_user({
                "email": user["email"],
                "password": user["password"],
                "email_confirm": True
            })
            
            # Créer l'utilisateur dans la table auth.users
            users_response = supabase.table('auth.users').insert({
                "id": auth_response.user.id,
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"],
                "disabled": user["disabled"],
                "created_at": user["created_at"],
                "updated_at": user["updated_at"],
                "deleted_at": user["deleted_at"],
                "last_login": user["last_login"]
            }).execute()

            # Ajouter le rôle dans la table user_roles
            roles_response = supabase.table('user_roles').insert({
                "user_id": auth_response.user.id,
                "role": user["role"],
                "group_id": user["group"]
            }).execute()
            
            print(f"Utilisateur {user['email']} créé avec succès dans auth.users et user_roles")
            time.sleep(1)  # Délai d'une seconde entre chaque création
        except Exception as e:
            print(f"Erreur lors de la création de {user['email']}: {str(e)}")
            print(f"Type d'erreur: {type(e)}")
            print(f"Arguments de l'erreur: {e.args}")
            if hasattr(e, 'response'):
                print(f"Response status: {e.response.status_code}")
                print(f"Response headers: {e.response.headers}")
                print(f"Response data: {e.response.data}")
            print(f"Traceback complet:")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("Début de la création des utilisateurs...")
    create_users()
    print("Aucun nouvel utilisateur n'a été créé - tous les utilisateurs existent déjà")
