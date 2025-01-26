from fastapi import APIRouter, Depends, HTTPException, Request, Header
from datetime import datetime, timedelta
import logging
from supabase import Client
from database import SUPABASE_JWT_SECRET, get_db, resolve_token
import uuid
from jose import JWTError, jwt

logger = logging.getLogger(__name__)

router = APIRouter( tags=["sessions"])

# --- Fonctions Utilitaires ---
def get_session(session_id: str, db: Client = Depends(get_db)):
    """Récupère une session par son ID"""
    response = db.table('sessions').select('*').eq('id', session_id).execute()
    return response.data[0] if response.data else None

# --- Routes ---
@router.post("/sessions/add")
async def create_session(
    session_data: dict, 
    authorization: str = Header(None),
    db: Client = Depends(get_db)
):
    """Crée une nouvelle session"""
    try:
        # Vérification du header Authorization
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token JWT manquant")
            
        # Extraction du token
        token = authorization.split(" ")[1]
        
        response = db.auth.get_session()

        # Décodage du JWT
        #user_id = resolve_token(token)
        user_id= response.user.id

        # Validation des données
        required_fields = ['name']
        if not all(field in session_data for field in required_fields):
            raise HTTPException(
                status_code=400,
                detail=f"Les champs suivants sont requis: {', '.join(required_fields)}"
            )

        # Valeur par défaut si aucune date n'est fournie
        #session_data['start_date'] = datetime.utcnow().isoformat()
        session_data['start_date'] = None

                
        #start_date = datetime.fromisoformat(session_data['start_date'])
        
        #session_data['end_date'] = (start_date + timedelta(hours=2)).isoformat()
        session_data['end_date'] = None

        # Création de la session
        session_data['status'] = 'idle'
        session_data['user_id'] = user_id
        
        # Conversion des dates en timestamp sans timezone
        #session_data['start_date'] = datetime.fromisoformat(session_data['start_date']).strftime('%Y-%m-%d %H:%M:%S')
        #session_data['end_date'] = datetime.fromisoformat(session_data['end_date']).strftime('%Y-%m-%d %H:%M:%S')
        
        response = db.table('sessions').insert(session_data).execute()
        
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Erreur lors de la création de la session")
    except Exception as e:
        # Log complet de l'erreur
        logger.error(f"Erreur création session: {e!r}", exc_info=True)
        
        # Extraction sécurisée du message d'erreur
        error_detail = "Erreur serveur"
        if hasattr(e, 'args') and e.args:
            if isinstance(e.args[0], dict) and 'message' in e.args[0]:
                error_detail = e.args[0]['message']
            elif isinstance(e.args[0], str):
                error_detail = e.args[0]
            elif len(e.args) > 1 and isinstance(e.args[1], str):
                error_detail = e.args[1]
        
        # Gestion des erreurs spécifiques
        if "duplicate" in str(error_detail).lower():
            error_detail = "Une session avec ces informations existe déjà"
        elif "null value" in str(error_detail).lower():
            error_detail = "Des informations obligatoires sont manquantes"
            
        raise HTTPException(
            status_code=400 if "duplicate" in str(error_detail).lower() else 500,
            detail=error_detail
        )

@router.get("/sessions/list")
async def get_sessions(db: Client = Depends(get_db)):
    """Récupère toutes les sessions"""
    try:
        response = db.table('sessions').select('*').execute()
        return response.data
    except Exception as e:
        logger.error(f"Erreur récupération sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la récupération des sessions")

@router.get("/sessions/{session_id}")
async def get_session_by_id(session_id: str, db: Client = Depends(get_db)):
    """Récupère une session par son ID"""
    try:
        # Validation de l'UUID
        uuid.UUID(session_id)
        
        session = get_session(session_id, db)
        if not session:
            raise HTTPException(status_code=404, detail="Session non trouvée")
            
        return session
    except ValueError:
        raise HTTPException(status_code=400, detail="ID session invalide")
    except Exception as e:
        logger.error(f"Erreur recherche session: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la recherche")

@router.put("/sessions/update/{session_id}")
async def update_session(session_id: str, updates: dict, db: Client = Depends(get_db)):
    """Met à jour une session existante"""
    try:
        # Validation de l'UUID
        uuid.UUID(session_id)
        
        # Vérification de l'existence de la session
        existing_session = get_session(session_id, db)
        if not existing_session:
            raise HTTPException(status_code=404, detail="Session non trouvée")
            
        # Mise à jour
        updates['updated_at'] = datetime.utcnow().isoformat()
        response = db.table('sessions').update(updates).eq('id', session_id).execute()
        
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Erreur lors de la mise à jour de la session")
    except ValueError:
        raise HTTPException(status_code=400, detail="ID session invalide")
    except Exception as e:
        logger.error(f"Erreur mise à jour session: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la mise à jour")

@router.delete("/sessions/delete/{session_id}")
async def delete_session(session_id: str, db: Client = Depends(get_db)):
    """Supprime une session"""
    try:
        # Validation de l'UUID
        uuid.UUID(session_id)
        
        # Suppression
        db.table('sessions').delete().eq('id', session_id).execute()
        return {"message": f"Session {session_id} supprimée avec succès"}
    except ValueError:
        raise HTTPException(status_code=400, detail="ID session invalide")
    except Exception as e:
        logger.error(f"Erreur suppression session: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la suppression")

@router.post("/sessions/start/{session_id}")
async def start_session(
    session_id: str,
    db: Client = Depends(get_db)
):
    """Démarre une session existante"""
    try:
        # Validation de l'UUID
        uuid.UUID(session_id)
        
        # Vérification de l'existence de la session
        session = get_session(session_id, db)
        if not session:
            raise HTTPException(status_code=404, detail="Session non trouvée")

        if session['status'] == 'started':
            raise HTTPException(status_code=400, detail="Session déjà démarrée")
            
        # Mise à jour de la session
        updates = {
            'status': 'started',
            'start_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        response = db.table('sessions').update(updates).eq('id', session_id).execute()
        
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Erreur lors du démarrage de la session")
    except ValueError:
        raise HTTPException(status_code=400, detail="ID session invalide")
    except Exception as e:
        detail="Erreur serveur lors du démarrage de la session"
        if e.status_code == 400:
            detail="Session déjà démarrée"
        logger.error(f"Erreur démarrage session: {e!r}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=detail
        )

@router.post("/sessions/stop/{session_id}")
async def stop_session(
    session_id: str,
    db: Client = Depends(get_db)
):
    """Arrête une session existante"""
    try:
        # Validation de l'UUID
        uuid.UUID(session_id)
        
        # Vérification de l'existence de la session
        session = get_session(session_id, db)
        if not session:
            raise HTTPException(status_code=404, detail="Session non trouvée")
            
        # Mise à jour de la session
        updates = {
            'status': 'stopped',
            'end_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        }
        if session['status'] == 'stopped':
            raise HTTPException(status_code=400, detail="Session déjà arrêtée")
        
        response = db.table('sessions').update(updates).eq('id', session_id).execute()
        
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Erreur lors de l'arrêt de la session")
    except ValueError:
        raise HTTPException(status_code=400, detail="ID session invalide")
    except Exception as e:
        detail="Erreur serveur lors de l'arrêt de la session"
        logger.error(f"Erreur arrêt session: {e!r}", exc_info=True)
        if e.status_code == 400:
            detail="Session déjà arrêtée"
        raise HTTPException(
            status_code=500,
            detail=detail
        )
