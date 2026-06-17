from typing import List, Optional
import os
import json

class CloudSearchService:
    """Service for searching files in cloud storage providers"""

    def __init__(self):
        self.google_drive_api_base = "https://www.googleapis.com/drive/v3"
        self.dropbox_api_base = "https://api.dropboxapi.com/2"

    def search_google_drive(self, query: str, auth_token: str) -> List[str]:
        """
        Search for files in Google Drive matching the query
        
        Args:
            query: Search query (file name or content)
            auth_token: Google Drive OAuth2 token
            
        Returns:
            List of matching file paths/names
        """
        try:
            import requests
        except ImportError:
            return []

        try:
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Accept": "application/json"
            }

            # Search for files containing the query in their name or content
            search_query = f"name contains '{query}' or fullText contains '{query}'"
            params = {
                "q": search_query,
                "spaces": "drive",
                "fields": "files(id, name, mimeType, webViewLink)",
                "pageSize": 50
            }

            response = requests.get(
                f"{self.google_drive_api_base}/files",
                headers=headers,
                params=params,
                timeout=10
            )

            if response.status_code != 200:
                return []

            data = response.json()
            results = []
            
            for file in data.get("files", []):
                # Skip folders
                if file.get("mimeType") == "application/vnd.google-apps.folder":
                    continue
                
                results.append(f"{file.get('name')} (Google Drive) - {file.get('webViewLink', '')}")

            return results

        except Exception:
            return []

    def search_dropbox(self, query: str, auth_token: str) -> List[str]:
        """
        Search for files in Dropbox matching the query
        
        Args:
            query: Search query (file name)
            auth_token: Dropbox OAuth2 token
            
        Returns:
            List of matching file paths
        """
        try:
            import requests
        except ImportError:
            return []

        try:
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "query": query,
                "options": {
                    "path": "/",
                    "max_results": 50,
                    "file_status": "active"
                }
            }

            response = requests.post(
                f"{self.dropbox_api_base}/files/search_v2",
                headers=headers,
                json=payload,
                timeout=10
            )

            if response.status_code != 200:
                return []

            data = response.json()
            results = []

            for match in data.get("matches", []):
                metadata = match.get("metadata", {})
                path = metadata.get("path_display", "")
                
                # Skip folders
                if metadata.get(".tag") == "folder":
                    continue
                
                if path:
                    results.append(f"{path} (Dropbox)")

            return results

        except Exception:
            return []

    def get_google_drive_auth_url(self, client_id: str, redirect_uri: str) -> str:
        """
        Generate Google Drive OAuth2 authentication URL
        
        Args:
            client_id: Google OAuth2 client ID
            redirect_uri: Redirect URI for OAuth callback
            
        Returns:
            Authentication URL
        """
        scopes = "https://www.googleapis.com/auth/drive.readonly"
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scopes}&"
            f"access_type=offline"
        )
        return auth_url

    def get_dropbox_auth_url(self, app_key: str, redirect_uri: str) -> str:
        """
        Generate Dropbox OAuth2 authentication URL
        
        Args:
            app_key: Dropbox app key
            redirect_uri: Redirect URI for OAuth callback
            
        Returns:
            Authentication URL
        """
        auth_url = (
            f"https://www.dropbox.com/oauth2/authorize?"
            f"client_id={app_key}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"token_access_type=offline"
        )
        return auth_url

    def exchange_google_drive_code(self, code: str, client_id: str, client_secret: str, redirect_uri: str) -> Optional[str]:
        """Exchange Google Drive authorization code for access token"""
        try:
            import requests
        except ImportError:
            return None

        try:
            payload = {
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            }

            response = requests.post(
                "https://oauth2.googleapis.com/token",
                data=payload,
                timeout=10
            )

            if response.status_code == 200:
                return response.json().get("access_token")
            
            return None

        except Exception:
            return None

    def exchange_dropbox_code(self, code: str, app_key: str, app_secret: str, redirect_uri: str) -> Optional[str]:
        """Exchange Dropbox authorization code for access token"""
        try:
            import requests
        except ImportError:
            return None

        try:
            payload = {
                "code": code,
                "grant_type": "authorization_code",
                "client_id": app_key,
                "client_secret": app_secret,
                "redirect_uri": redirect_uri
            }

            response = requests.post(
                "https://api.dropboxapi.com/oauth2/token",
                data=payload,
                timeout=10
            )

            if response.status_code == 200:
                return response.json().get("access_token")
            
            return None

        except Exception:
            return None
