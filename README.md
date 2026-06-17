# EasyCode

EasyCode is a local-first AI coding assistant MVP built with FastAPI and a VS Code extension integration. It supports code understanding, search, diff generation, and patch application through a local backend.

## Project Structure

- `backend/`: FastAPI backend server
- `editor-extension/`: VS Code extension scaffold and client code
- `docs/`: architecture, API, and roadmap documentation
- `scripts/`: helper scripts for environment setup and utilities

## Prerequisites

- Python 3.11+
- Node.js 20+ and npm
- Git
- Optional: VS Code for extension development

## Setup

1. Clone the repository if needed:
   ```powershell
   git clone https://github.com/mishu-anik23/easycode.git
   cd easycode
   ```

2. Create a Python virtual environment and install backend dependencies:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r backend/requirements.txt
   ```

3. Create the `.env` file from the example:
   ```powershell
   python scripts\setup_env.py
   ```

4. Install the VS Code extension dependencies:
   ```powershell
   cd editor-extension
   npm install
   cd ..
   ```

## Run the Backend

From the repository root with the virtual environment active:

```powershell
uvicorn backend.app.main:app --reload --port 8000
```

The backend API will be available at `http://127.0.0.1:8000`.

## Run the VS Code Extension

1. Open `editor-extension/` in VS Code.
2. Run `npm run compile` to build the extension sources.
3. Press `F5` to launch the extension in a new Extension Development Host window.

## Use the Extension

After launching the extension, run one of the commands from the Command Palette:

- `EasyCode: Start Chat` - Start a chat session with AI assistant
- `EasyCode: Search Codebase` - Search in current repository
- `EasyCode: Search Folders (Local/Google Drive/Dropbox)` - Search in specific folders with cloud storage support
- `EasyCode: Generate Diff` - Generate code changes based on your description
- `EasyCode: Apply Diff` - Apply generated diffs to files

## New Features

### Enhanced Chat Error Handling
- Automatic retry logic (3 retries with exponential backoff)
- Better error messages when backend is unavailable
- Connection status feedback to users

### Multi-Source Folder Search
Search for code across multiple storage sources:

#### Local Folder Search
- Browse and select any folder on your local machine
- Search across common code file types (.py, .js, .ts, .java, .cpp, .go, .rs, etc.)
- Results show file path and line number

#### Google Drive Integration
- Authenticate with your Google account
- Search through Google Drive for code files
- Supports searching by file name and content

#### Dropbox Integration
- Authenticate with Dropbox account
- Search through Dropbox files
- Get direct Dropbox links to results

## Cloud Storage Setup

For detailed setup instructions including OAuth2 configuration for Google Drive and Dropbox:

See [SETUP_GUIDE.md](SETUP_GUIDE.md)

## Features in Development

- Enhanced cloud storage caching
- Real-time file indexing
- Advanced filtering options
- Batch operations support

## Testing

Run backend tests from the repository root:

```powershell
pytest backend/tests
```

## Environment Configuration

The `.env.example` file contains default backend settings:

- `PROJECT_ID=easycode`
- `DATABASE_URL=sqlite:///./easycode.db`
- `OLLAMA_URL=http://127.0.0.1:11434`
- `MODEL_NAME=qwen2.5-coder-7b`

Adjust `.env` as needed for your local environment.

## Notes

- The backend currently uses FastAPI with CORS enabled for local development.
- The VS Code extension communicates with the backend via the local API.
- If you already have a `.env` file, `scripts/setup_env.py` will not override it.
