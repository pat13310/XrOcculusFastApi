import jwt

def verify_jwt(token: str, secret: str) -> dict:
    """
    Vérifie et décode un token JWT
    
    Args:
        token (str): Le token JWT à vérifier
        secret (str): La clé secrète pour vérifier la signature
        
    Returns:
        dict: Le payload décodé
        
    Raises:
        jwt.ExpiredSignatureError: Si le token est expiré
        jwt.InvalidTokenError: Si le token est invalide
        Exception: Pour toute autre erreur
    """
    try:
        return jwt.decode(token, secret, algorithms=["HS256"], audience="authenticated")
    except jwt.ExpiredSignatureError:
        print("Erreur: Le token est expiré.")
        raise
    except jwt.InvalidTokenError:
        print("Erreur: Le token est invalide.") 
        raise
    except Exception as e:
        print(f"Erreur: {e}")
        raise

# Token JWT Supabase fourni
supabase_token = "eyJhbGciOiJIUzI1NiIsImtpZCI6IlR1MENtc05jOXZPZjFNMXIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FsdnJmZGN1dHpsa3Zyb3NveXlqLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJhYjA3YzE5Yy1kY2RlLTQyYTMtODA4MS1kNmZlZmM2NTBhNjEiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM3OTk0MDkxLCJpYXQiOjE3Mzc5ODY4OTEsImVtYWlsIjoiZGVtbzJAZXhhbXBsZS5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoiZGVtbzJAZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiJhYjA3YzE5Yy1kY2RlLTQyYTMtODA4MS1kNmZlZmM2NTBhNjEifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTczNzk4Njg5MX1dLCJzZXNzaW9uX2lkIjoiODNlY2M4NzktZTY5ZS00OWQ1LWEyOGYtZGU4MmNjYmMxM2RhIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.oJfZnbhxbH77DeLJLwoarwVG_l1jxQMPN9VIQXHJTOw"

# Clé secrète Supabase (décodée correctement en base64)
supabase_jwt_secret = "VO84MJU8O+D6aO3W5tyHbjLwTQQNIAIRyl/OB8iq4ukPyA0RlOzlAskpznY2FC6xA9d9EBHjKLWCVPnehs+bdw=="

# Vérification du token avec la nouvelle fonction
try:
    decoded_payload = verify_jwt(supabase_token, supabase_jwt_secret)
    print("Le token est valide!")
    print(decoded_payload)
except:
    print("Échec de la vérification du token")
