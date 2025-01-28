import json
import logging
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from config import Settings
from fastapi.middleware.cors import CORSMiddleware

# Importer le routeur auth et les fonctions utilitaires
from routes.users import router as user_router
from routes.groups import router as group_router
from routes.session import router as session_router
from routes.devices import router as device_router
from routes.system import router as system_router
from routes.applications import router as application_router
from routes.message import router as phone_router
from routes.screen import router as screen_router
from routes.comments import router as comment_router


from database import get_db

from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

# Configurer le journal
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Charger la configuration depuis un fichier externe
config = Settings.load_config()

# Initialisation de l'application FastAPI
app = FastAPI()

# Configuration CORS - doit être avant l'inclusion des routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
    expose_headers=["*"],
    max_age=3600,
)

# Inclure les routeurs
app.include_router(user_router, dependencies=[Depends(get_db)])
app.include_router(group_router, dependencies=[Depends(get_db)])
app.include_router(session_router, dependencies=[Depends(get_db)])
app.include_router(device_router, dependencies=[Depends(get_db)])
app.include_router(system_router, dependencies=[Depends(get_db)])
app.include_router(application_router, dependencies=[Depends(get_db)])
#app.include_router(phone_router, dependencies=[Depends(get_db)])
#app.include_router(screen_router,dependencies=[Depends(get_db)])
# app.include_router(comment_router, dependencies=[Depends(get_db)])

# Modèle Pydantic pour la connexion
class LoginRequest(BaseModel):
    email: str
    password: str

def get_user(db, username: str):
    try:
        # Vérifier si la table auth.users existe
        result = db.table("auth.users").select("*").eq("email", username).execute()
        if result.data:
            return result.data[0]
        return None
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'utilisateur: {str(e)}")
        return None

# Route de login
@app.post("/auth/login")
async def login(request: Request, db = Depends(get_db)):
    try:
        # Log de la requête entrante
        body = await request.json()
        email = body.get('email')
        password = body.get('password')
        
        logger.info(f"Tentative de connexion pour l'email: {email}")
        
        if not email or not password:
            logger.error("Email ou mot de passe manquant")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email et mot de passe requis"
            )
        
        try:
            # Tentative de connexion avec Supabase
            response = db.auth.sign_in_with_password({
                "email": email, 
                "password": password
            })
            
            # Vérification de la réponse
            if not response or not response.user:
                logger.error(f"Échec de l'authentification pour {email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Identifiants invalides"
                )
            
            
            # Préparer les informations utilisateur
            user_data = {
                "email": response.user.email,
                "id": response.user.id,
                # Ajoutez d'autres informations utilisateur si nécessaire
            }
            
            logger.info(f"Connexion réussie pour {email}")
            
            return {
                "access_token": response.session.access_token,
                "token_type": "bearer",
                "user": user_data
            }
        
        except Exception as auth_error:
            logger.error(f"Erreur d'authentification Supabase: {str(auth_error)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Erreur d'authentification"
            )
    
    except HTTPException as http_error:
        # Réacheminement des exceptions HTTP
        logger.error(f"Erreur HTTP: {http_error.detail}")
        raise
    
    except Exception as unexpected_error:
        # Gestion des erreurs inattendues
        logger.error(f"Erreur inattendue lors de la connexion: {str(unexpected_error)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erreur interne du serveur"
        )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
blacklist = set()

# --- Dépendances ---
async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    try:
        payload = jwt.decode(token, config.get("SECRET_KEY"), algorithms=config.get("ALGORITHM"))
        username: str = payload.get("sub")
        if username is None or token in blacklist:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(db, username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

async def get_current_active_user(current_user = Depends(get_current_user)):
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Route de logout
@app.post("/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    blacklist.add(token)
    return {"message": "Déconnexion réussie"}

# Route de mot de passe oublié
@app.post("/auth/forgot-password")
async def forgot_password(request: Request, db = Depends(get_db)):
    body = await request.json()
    email = body.get('email')
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email requis"
        )
    
    try:
        logger.info(f"Envoi d'email de réinitialisation pour: {email}")
        db.auth.reset_password_for_email(email)
        return {
            "message": "Si l'email existe dans notre système, vous recevrez un email de réinitialisation",
            "email": email
        }
    except Exception as error:
        logger.error(f"Erreur lors de l'envoi d'email: {str(error)}")
        # On retourne quand même un succès pour ne pas révéler si l'email existe
        return {
            "message": "Si l'email existe dans notre système, vous recevrez un email de réinitialisation",
            "email": email
        }

# Route racine
@app.get("/")
async def read_root():
    return {
        "message": "Bienvenue sur l'API XrOcculus FastAPI avec supabase",
        "version": config.get("version", "1.0.2"),
        "date_de_creation": "2025-01-25",
        "auteur": "XenDev"
    }

# Route de santé
@app.get("/health")
async def health_check():
    from datetime import datetime
    return {
        "status": "ok",
        "time": datetime.now().isoformat()
    }

# Middleware pour gérer les erreurs 404
@app.middleware("http")
async def custom_404_handler(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Ressource non trouvée",
                            }
        )
    return response

# Gestionnaire d'erreurs personnalisé pour les erreurs HTTP
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

# Route de développement pour Swagger UI
@app.get("/dev/swagger", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger UI")

# Route de développement pour ReDoc
@app.get("/dev/doc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(openapi_url="/openapi.json", title="ReDoc")

# Démarrage du serveur
if __name__ == '__main__':
    import uvicorn
    logger.info("Démarrage du serveur FastAPI")
    logger.debug(f"Host: {config.get('host', '0.0.0.0')}, Port: {config.get('port', 8000)}, Reload: {config.get('reload', True)}")
    uvicorn.run("main:app", 
                host=config.get("host", "0.0.0.0"), 
                port=config.get("port", 8000), 
                reload=config.get("reload", True),
                log_level="debug")
