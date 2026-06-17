# EasyCode API Documentation

## Base URL
```
http://127.0.0.1:8000
```

## Authentication

Most endpoints require a `project_id` in the request body. Cloud storage endpoints additionally require authentication tokens obtained through the auth endpoints.

## Endpoints

### Health Check

#### GET `/`
Returns the status of the backend API.

**Response:**
```json
{
  "status": "EasyCode backend is running"
}
```

---

## Chat Endpoints

### POST `/chat/`
Send a message to the AI assistant.

**Request Body:**
```json
{
  "project_id": "easycode",
  "message": "What does this function do?",
  "selected_files": ["src/utils.py"],
  "mode": "chat"
}
```

**Response:**
```json
{
  "reply": "This function...",
  "used_context": ["src/utils.py"],
  "tokens": 150
}
```

---

## Search Endpoints

### POST `/search/`
Search the repository codebase.

**Request Body:**
```json
{
  "project_id": "easycode",
  "query": "function_name",
  "search_source": "local"
}
```

**Response:**
```json
{
  "results": [
    "src/file.py:42: def function_name():",
    "src/other.py:15: function_name(arg)"
  ]
}
```

### POST `/search/folder/local`
Search for code in a local folder.

**Request Body:**
```json
{
  "project_id": "easycode",
  "folder_path": "/path/to/folder",
  "query": "search_term"
}
```

**Response:**
```json
{
  "results": [
    "file.py:10: matching line content",
    "other.py:25: another match"
  ],
  "source": "local"
}
```

### POST `/search/folder/google-drive`
Search for code files in Google Drive.

**Request Body:**
```json
{
  "project_id": "easycode",
  "query": "filename",
  "auth_token": "google_oauth_access_token"
}
```

**Response:**
```json
{
  "results": [
    "script.py (Google Drive) - https://drive.google.com/file/d/...",
    "module.py (Google Drive) - https://drive.google.com/file/d/..."
  ],
  "source": "google_drive"
}
```

### POST `/search/folder/dropbox`
Search for code files in Dropbox.

**Request Body:**
```json
{
  "project_id": "easycode",
  "query": "filename",
  "auth_token": "dropbox_oauth_access_token"
}
```

**Response:**
```json
{
  "results": [
    "/Scripts/main.py (Dropbox)",
    "/Utils/helpers.py (Dropbox)"
  ],
  "source": "dropbox"
}
```

---

## Authentication Endpoints

### POST `/auth/google-drive/url`
Get Google Drive OAuth2 authentication URL.

**Request Body:**
```json
{
  "project_id": "easycode"
}
```

**Response:**
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=...&response_type=code&scope=..."
}
```

### POST `/auth/dropbox/url`
Get Dropbox OAuth2 authentication URL.

**Request Body:**
```json
{
  "project_id": "easycode"
}
```

**Response:**
```json
{
  "auth_url": "https://www.dropbox.com/oauth2/authorize?client_id=...&redirect_uri=...&response_type=code"
}
```

### GET `/auth/google-drive/callback`
Handle Google Drive OAuth2 callback (redirect from OAuth provider).

**Query Parameters:**
- `code` (string): Authorization code from Google
- `state` (string, optional): State parameter for CSRF protection

**Response:**
```json
{
  "token": "access_token_string",
  "success": true
}
```

### GET `/auth/dropbox/callback`
Handle Dropbox OAuth2 callback (redirect from OAuth provider).

**Query Parameters:**
- `code` (string): Authorization code from Dropbox
- `state` (string, optional): State parameter for CSRF protection

**Response:**
```json
{
  "token": "access_token_string",
  "success": true
}
```

---

## Diff Endpoints

### POST `/diff/`
Generate a unified diff based on a description.

**Request Body:**
```json
{
  "project_id": "easycode",
  "goal": "Add error handling to the login function",
  "files": ["src/auth.py"]
}
```

**Response:**
```json
{
  "diff": "--- a/src/auth.py\n+++ b/src/auth.py\n@@ -10,2 +10,5 @@\n try:\n-    user = db.get_user(email)\n+    user = db.get_user(email)\n+    if not user:\n+        return None\n except Exception as e:\n     logger.error(e)"
}
```

---

## Apply Endpoints

### POST `/apply/`
Apply a unified diff to files in the project.

**Request Body:**
```json
{
  "project_id": "easycode",
  "diff": "--- a/file.py\n+++ b/file.py\n@@ -1,3 +1,3 @@..."
}
```

**Response:**
```json
{
  "status": "applied successfully"
}
```

---

## Plan Endpoints

### POST `/plan/`
Generate a plan for implementing changes.

**Request Body:**
```json
{
  "project_id": "easycode",
  "goal": "Implement user authentication",
  "files": ["src/main.py", "src/db.py"]
}
```

**Response:**
```json
{
  "plan": "1. Design database schema...\n2. Create authentication routes...\n3. Add middleware..."
}
```

---

## Index Endpoints

### POST `/index/`
Index repository files for better search performance.

**Request Body:**
```json
{
  "project_id": "easycode"
}
```

**Response:**
```json
{
  "status": "indexing started",
  "files_found": 42
}
```

---

## Error Responses

All endpoints may return error responses in this format:

```json
{
  "detail": "Error description"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `403`: Forbidden (authentication required)
- `404`: Not Found
- `503`: Service Unavailable (backend service not available)

---

## Rate Limiting

Currently, there are no rate limits implemented. Production deployments should add rate limiting.

---

## CORS

CORS is enabled for all origins (`*`) in development. This should be restricted in production.

---

## WebSockets

WebSocket support for real-time features is planned for future versions.

---

## Examples

### Using cURL

#### Search the codebase:
```bash
curl -X POST http://127.0.0.1:8000/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "easycode",
    "query": "async"
  }'
```

#### Start a chat:
```bash
curl -X POST http://127.0.0.1:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "easycode",
    "message": "Explain this code",
    "selected_files": ["app.py"],
    "mode": "chat"
  }'
```

#### Search local folder:
```bash
curl -X POST http://127.0.0.1:8000/search/folder/local \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "easycode",
    "folder_path": "/home/user/projects/myapp",
    "query": "database"
  }'
```

### Using Python

```python
import requests

# Chat
response = requests.post(
    'http://127.0.0.1:8000/chat/',
    json={
        'project_id': 'easycode',
        'message': 'What does this file do?',
        'selected_files': ['main.py'],
        'mode': 'chat'
    }
)
print(response.json())

# Search
response = requests.post(
    'http://127.0.0.1:8000/search/',
    json={
        'project_id': 'easycode',
        'query': 'function_name'
    }
)
print(response.json()['results'])
```
