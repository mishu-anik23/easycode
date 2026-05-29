# EasyCode VS Code Extension

EasyCode integrates VS Code with the local EasyCode backend to provide AI-assisted coding workflows.

## Features

- Start a chat with the EasyCode backend
- Search the repository for code matches
- Generate diffs for requested changes
- Apply unified diffs directly from VS Code

## Usage

1. Start the EasyCode backend:
   ```powershell
   uvicorn backend.app.main:app --reload --port 8000
   ```
2. Open VS Code and run the command palette.
3. Use `EasyCode: Start Chat` to ask a coding question.
4. Use `EasyCode: Search Codebase` to search repository content.
5. Use `EasyCode: Generate Diff` to create a change diff.
6. Use `EasyCode: Apply Diff` to apply a unified diff.

## Configuration

The extension communicates with the backend at `http://127.0.0.1:8000` by default. You can update the URL in `src/api.ts`.
