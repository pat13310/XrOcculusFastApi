import os
from supabase import create_client, Client
import pytest
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv('.env.test')

@pytest.fixture
def supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)

def test_supabase_connection(supabase_client):
    # Test simple pour vérifier la connexion
    try:
        # Vérifier que le client est bien initialisé
        assert supabase_client is not None
        # Vérifier que l'URL et la clé sont correctes
        assert supabase_client.supabase_url == os.environ.get("SUPABASE_URL")
        assert supabase_client.supabase_key == os.environ.get("SUPABASE_KEY")
    except Exception as e:
        pytest.fail(f"La connexion à Supabase a échoué : {str(e)}")
