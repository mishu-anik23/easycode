# EasyCode Backend Setup Guide

## Prerequisites

- Python 3.8+
- pip or conda
- Ollama (for local LLM)
- Node.js 14+ (for extension)

## Backend Setup

### 1. Install Dependencies

```bash
cd backend

```

### 2. Configure Environment

Create a `.env` file in the backend directory:

```env
PROJECT_ROOT=./
OLLAMA_BASE_URL=http://localhost:11434
GOOGLE_DRIVE_CLIENT_ID=your_google_client_id
GOOGLE_DRIVE_CLIENT_SECRET=your_google_client_secret
GOOGLE_DRIVE_REDIRECT_URI=http://localhost:8000/auth/google-drive/callback
DROPBOX_APP_KEY=your_dropbox_app_key
DROPBOX_APP_SECRET=your_dropbox_app_secret
DROPBOX_REDIRECT_URI=http://localhost:8000/auth/dropbox/callback
```

### 3. Start Ollama Service

```bash
ollama serve
```

In another terminal, pull a model:

```bash
ollama pull mistral
```

### 4. Start the Backend Server

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at `http://127.0.0.1:8000`

## Google Drive Integration

### Setup OAuth2 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Drive API
4. Create OAuth2 credentials (Authorized redirect URIs):
   - `http://localhost:8000/auth/google-drive/callback`
   - `http://localhost:3000/auth/google-drive/callback` (for VS Code extension)
5. Copy Client ID and Client Secret to `.env`

## Dropbox Integration

### Setup OAuth2 Credentials

1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Create a new app
3. Set Redirect URIs:
   - `http://localhost:8000/auth/dropbox/callback`
   - `http://localhost:3000/auth/dropbox/callback`
4. Copy App Key and App Secret to `.env`

## Extension Setup

### 1. Install Dependencies

```bash
cd editor-extension
npm install
```

### 2. Build Extension

```bash
npm run compile
```

### 3. Debug/Run Extension

- Open the extension folder in VS Code
- Press F5 to open the extension in a new window
- Commands available:
  - `EasyCode: Start Chat` - Start a chat session
  - `EasyCode: Search Codebase` - Search in current repository
  - `EasyCode: Search Folders (Local/Google Drive/Dropbox)` - Search in specific folders
  - `EasyCode: Generate Diff` - Generate code changes
  - `EasyCode: Apply Diff` - Apply generated diffs

## API Endpoints

### Chat
- `POST /chat/` - Send a chat message

### Search
- `POST /search/` - Search in codebase
- `POST /search/folder/local` - Search in local folder
- `POST /search/folder/google-drive` - Search in Google Drive
- `POST /search/folder/dropbox` - Search in Dropbox

### Authentication
- `POST /auth/google-drive/url` - Get Google Drive auth URL
- `POST /auth/dropbox/url` - Get Dropbox auth URL
- `GET /auth/google-drive/callback` - Google Drive OAuth callback
- `GET /auth/dropbox/callback` - Dropbox OAuth callback

### Diff & Apply
- `POST /diff/` - Generate diff
- `POST /apply/` - Apply diff

## Troubleshooting

### "Cannot connect to EasyCode backend" Error

1. Ensure backend server is running on `http://127.0.0.1:8000`
2. Check firewall settings
3. Verify the server is not crashing (check terminal output)

### Cloud Storage Issues

- Ensure OAuth credentials are correct in `.env`
- Check that redirect URIs match exactly in OAuth configuration
- Tokens should be obtained through the auth endpoints before searching

## Features

### Local Folder Search
- Search in any local directory
- Supports multiple file types (.py, .js, .ts, .java, .cpp, .go, .rs, etc.)
- Results include file path and line number

### Google Drive Search
- Search through Google Drive files
- Requires OAuth authentication
- Searches by file name and content

### Dropbox Search
- Search through Dropbox files
- Requires OAuth authentication
- Returns file paths with Dropbox links

## Error Handling

The extension includes:
- **Retry logic** for connection failures (3 retries with 1s delay)
- **Clear error messages** for troubleshooting
- **Graceful fallbacks** if cloud services are unavailable
- **Detailed logging** in the output channel

## Development

### Adding New Search Sources

1. Add methods to `CloudSearchService` in `backend/app/services/cloud_search_service.py`
2. Add API endpoint in `backend/app/api/search.py`
3. Add command handler in `editor-extension/src/extension.ts`
4. Update `package.json` with new command

### Extending Authentication

Modify `backend/app/api/auth.py` to support additional OAuth providers.
