from fastapi import APIRouter
from ..core.config import settings
from ..schemas.search import AuthUrlResponse
from ..services.cloud_search_service import CloudSearchService

router = APIRouter()
cloud_service = CloudSearchService()

@router.post("/google-drive/url")
def get_google_drive_auth_url(request: dict) -> AuthUrlResponse:
    """Get Google Drive OAuth2 authentication URL"""
    try:
        # Get credentials from config or environment
        client_id = getattr(settings, 'google_drive_client_id', None)
        redirect_uri = getattr(settings, 'google_drive_redirect_uri', 'http://localhost:8000/auth/google-drive/callback')
        
        if not client_id:
            raise ValueError("Google Drive client ID not configured")
        
        auth_url = cloud_service.get_google_drive_auth_url(client_id, redirect_uri)
        return AuthUrlResponse(auth_url=auth_url)
    except Exception as e:
        return AuthUrlResponse(auth_url="")

@router.post("/dropbox/url")
def get_dropbox_auth_url(request: dict) -> AuthUrlResponse:
    """Get Dropbox OAuth2 authentication URL"""
    try:
        # Get credentials from config or environment
        app_key = getattr(settings, 'dropbox_app_key', None)
        redirect_uri = getattr(settings, 'dropbox_redirect_uri', 'http://localhost:8000/auth/dropbox/callback')
        
        if not app_key:
            raise ValueError("Dropbox app key not configured")
        
        auth_url = cloud_service.get_dropbox_auth_url(app_key, redirect_uri)
        return AuthUrlResponse(auth_url=auth_url)
    except Exception as e:
        return AuthUrlResponse(auth_url="")

@router.get("/google-drive/callback")
def google_drive_callback(code: str, state: str = None):
    """Handle Google Drive OAuth2 callback"""
    try:
        client_id = getattr(settings, 'google_drive_client_id', None)
        client_secret = getattr(settings, 'google_drive_client_secret', None)
        redirect_uri = getattr(settings, 'google_drive_redirect_uri', 'http://localhost:8000/auth/google-drive/callback')
        
        if not (client_id and client_secret):
            return {"error": "Google Drive credentials not configured"}
        
        token = cloud_service.exchange_google_drive_code(code, client_id, client_secret, redirect_uri)
        
        if token:
            return {"token": token, "success": True}
        else:
            return {"error": "Failed to exchange authorization code", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

@router.get("/dropbox/callback")
def dropbox_callback(code: str, state: str = None):
    """Handle Dropbox OAuth2 callback"""
    try:
        app_key = getattr(settings, 'dropbox_app_key', None)
        app_secret = getattr(settings, 'dropbox_app_secret', None)
        redirect_uri = getattr(settings, 'dropbox_redirect_uri', 'http://localhost:8000/auth/dropbox/callback')
        
        if not (app_key and app_secret):
            return {"error": "Dropbox credentials not configured"}
        
        token = cloud_service.exchange_dropbox_code(code, app_key, app_secret, redirect_uri)
        
        if token:
            return {"token": token, "success": True}
        else:
            return {"error": "Failed to exchange authorization code", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}
