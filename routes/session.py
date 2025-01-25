from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
import logging
from supabase import Client
from database import get_db
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sessions", tags=["sessions"])

# --- Fonctions Utilitaires ---
def get_session(session_id: str, db: Client = Depends(get_db)):
    """Récupère une session par son ID"""
    response = db.table('sessions').select('*').eq('id', session_id).execute()
    return response.data[0] if response.data else None

# --- Routes ---
@router.post("sessions/add")
async def create_session(session_data: dict, db: Client = Depends(get_db)):
    """Crée une nouvelle session"""
    try:
        # Validation des données
        required_fields = ['name', 'start_time', 'end_time']
        if not all(field in session_data for field in required_fields):
            raise HTTPException(
                status_code=400,
                detail=f"Les champs suivants sont requis: {', '.join(required_fields)}"
            )

        # Création de la session
        session_data['id'] = str(uuid.uuid4())
        session_data['created_at'] = datetime.utcnow().isoformat()
        
        response = db.table('sessions').insert(session_data).execute()
        
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Erreur lors de la création de la session")
    except Exception as e:
        logger.error(f"Erreur création session: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la création de la session")

@router.get("sessions/list")
async def get_sessions(db: Client = Depends(get_db)):
    """Récupère toutes les sessions"""
    try:
        response = db.table('sessions').select('*').execute()
        return response.data
    except Exception as e:
        logger.error(f"Erreur récupération sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la récupération des sessions")

@router.get("sessions/{session_id}")
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

@router.put("sessions/update/{session_id}")
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

@router.delete("sessions/delete/{session_id}")
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
