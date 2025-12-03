import secrets

from fastapi import Cookie, Depends, HTTPException, status,Request
from config import settings

admin_sessions = {}

def authenticate_admin(username, password):
    correct_username = secrets.compare_digest(username, settings.ADMIN_USER_NAME)
    correct_password = secrets.compare_digest(password, settings.ADMIN_PASSWORD)
    if correct_username and correct_password:
        token = secrets.token_hex(16) 
        admin_sessions[token] = True
        return token
    else:
        return None

def delete_admin_session(token):
    del admin_sessions[token]

from starlette.middleware.base import BaseHTTPMiddleware
class AdminSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, handler):
        admin_session_token = request.cookies.get("admin_session")
        request.state.is_admin = admin_session_token in admin_sessions
        response = await handler(request)
        return response

from fastapi.responses import JSONResponse
class AdminAuthzMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, handler):
        if request.method != "GET" and 'job-boards' in request.url.path and \
            (not hasattr(request.state, "is_admin") or not request.state.is_admin):
            return JSONResponse({}, status_code=status.HTTP_401_UNAUTHORIZED)
        response = await handler(request)
        return response
        
def is_admin(admin_session_token):
    return admin_session_token in admin_sessions
    
def require_admin(admin_session: str = Cookie(None)):
    if not admin_session or not is_admin(admin_session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin login required"
        )
    return True