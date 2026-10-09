from passlib.context import CryptContext
from datetime import datetime, timedelta
import secrets
from sqlalchemy.orm import Session
from models import Session as DBSession, User
import hashlib

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token():
    return secrets.token_hex(32)

def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()

def create_session(db: Session, user_id: int, ip_address: str, user_agent: str, expires_delta: timedelta = timedelta(days=1)):
    token = create_access_token()
    token_hash = hash_token(token)
    session_id = secrets.token_hex(16)
    
    expires_at = datetime.utcnow() + expires_delta
    
    db_session = DBSession(
        id=session_id,
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return token, db_session
