from sqlalchemy.orm import Session
from models.models import User
from utils import hash_password
from datetime import datetime, timezone
from database import SessionLocal

def create_admin():
    """Crée un administrateur au démarrage."""
    db: Session = SessionLocal()
    admin_username = "admin"
    admin_email = "admin@example.com"
    admin_password = "adminpassword"
    admin_role = "admin"

    existing_user = db.query(User).filter(User.username == admin_username).first()
    if existing_user:
        print("L'administrateur existe déjà.")
        return

    hashed_password = hash_password(admin_password)
    new_admin = User(
        username=admin_username,
        email=admin_email,
        full_name="Admin User",
        hashed_password=hashed_password,
        role=admin_role,
        group=-1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    print("Administrateur créé avec succès.")

if __name__ == "__main__":
    create_admin()
