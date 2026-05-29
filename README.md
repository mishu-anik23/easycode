# EasyCode

EasyCode is a local-first AI coding assistant MVP built with FastAPI and a VS Code extension integration. It is designed to support code understanding, navigation, diff generation, and patch application using a lightweight local architecture.

## Structure

- `backend/`: FastAPI backend server
- `editor-extension/`: VS Code extension scaffolding
- `docs/`: architecture and API documentation
- `scripts/`: helper scripts for running and setup

## Getting Started

1. Install Python dependencies:
   ```powershell
   python -m pip install -r backend/requirements.txt
   ```
2. Start the backend:
   ```powershell
   uvicorn backend.app.main:app --reload --port 8000
   ```
3. Open the VS Code extension folder in VS Code or use the editor-extension scaffolding.
