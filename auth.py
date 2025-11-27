import secrets

from fastapi import Cookie, Depends, HTTPException, status,Request
from config import settings

admin_sessions = {}

def authenticate_admin(username, password):
    correct_username = secrets.compare_digest(username, settings.ADMIN_USERNAME)
    correct_password = secrets.compare_digest(password, settings.ADMIN_PASSWORD)
    if correct_username and correct_password:
        token = secrets.token_hex(16) 
        admin_sessions[token] = True
        return token
    else:
        return None

def is_admin(admin_session_token):
    return admin_session_token in admin_sessions
    
def require_admin(admin_session: str = Cookie(None)):
    if not admin_session or not is_admin(admin_session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin login required"
        )
    return True