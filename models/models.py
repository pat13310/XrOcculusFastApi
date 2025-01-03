from sqlalchemy import Column, String, Boolean, DateTime, func, Integer, ForeignKey, Table
from database import Base
from sqlalchemy.orm import relationship

# Table de correspondance entre les utilisateurs et les sessions
user_session_association = Table(
    'user_session_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('session_id', Integer, ForeignKey('sessions.id'))
)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    state = Column(String, default="inactive")
    users = relationship("User", secondary=user_session_association, back_populates="sessions")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    role = Column(String, default="user")
    group = Column(Integer, default=-1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    sessions = relationship("Session", secondary=user_session_association, back_populates="users")