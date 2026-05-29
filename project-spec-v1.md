# Open-Source AI Coding Assistant MVP

## Overview
Build a local-first AI coding assistant similar to Cursor, but focused on a lightweight MVP that runs on a developer machine and works with an AI editor or a VS Code extension. The system uses FastAPI for orchestration, Ollama for local model serving, Qwen2.5-Coder as the coding model, and a local index/search layer for repository context.

## Goals
- Assist with code understanding, navigation, and edits.
- Generate safe, reviewable diffs instead of direct file overwrites.
- Work offline or with minimal external dependencies.
- Stay lightweight enough for a modest local machine.
- Provide a clean backend API that any AI editor can call.

## Non-Goals
- Full Cursor replacement in version 1.
- Autonomous code execution without user approval.
- Complex multi-agent frameworks.
- Cloud dependency for core features.

## Recommended Model
Use `Qwen2.5-Coder-7B` first for the best balance of quality and local feasibility. If your machine is weaker, use a smaller Qwen2.5-Coder variant; if stronger, you can later move up to a larger quantized model. The assistant should support any Ollama-compatible open model [web:18].

## MVP Feature Set
1. Chat with selected file context.
2. Explain current file or symbol.
3. Search codebase with ripgrep and semantic search.
4. Generate diffs for one or more files.
5. Apply diffs after review.
6. Re-index project on demand.
7. Save session history and task checkpoints.
8. Optional terminal command suggestions with confirmation.

## System Architecture

### 1. Editor Layer
This can be implemented as:
- A VS Code extension.
- A custom Electron app.
- A Tauri app.
- Any AI editor that can call HTTP APIs.

Responsibilities:
- Capture user prompt.
- Send selected files or code snippets.
- Display model responses.
- Show diffs and allow apply/undo.

### 2. Backend Layer
Use FastAPI as the orchestration server.

Responsibilities:
- Accept prompts from the editor.
- Build context from files and repo search.
- Query the model.
- Generate structured outputs.
- Return diffs and plans.
- Manage sessions, history, and project metadata.

### 3. Model Layer
Use Ollama as the local inference runtime.

Responsibilities:
- Serve Qwen2.5-Coder via local HTTP API.
- Keep model management simple.
- Allow easy model switching later.

### 4. Retrieval Layer
Use a hybrid code context system.

Responsibilities:
- Fast file search using ripgrep.
- Symbol/file parsing for basic navigation.
- Optional embeddings-based semantic search.
- Chunking and ranking of relevant context.

### 5. Patch Layer
Use diff-based edits.

Responsibilities:
- Ask the model to output unified diffs or file patch objects.
- Validate patch format.
- Apply only after user approval.
- Support rollback.

## Suggested Tech Stack
- **Frontend/editor**: VS Code extension first.
- **Backend**: FastAPI + Uvicorn.
- **LLM runtime**: Ollama.
- **Model**: Qwen2.5-Coder 7B.
- **Search**: ripgrep, AST parsers if needed.
- **Vector store**: Chroma or SQLite with embeddings.
- **Database**: SQLite for sessions, tasks, checkpoints.
- **Language**: Python for backend, TypeScript for editor integration.
- **Diff handling**: unified diff, git apply.

## Repository Layout
```text
ai-coding-assistant/
├─ README.md
├─ .gitignore
├─ .env.example
├─ pyproject.toml
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ api/
│  │  │  ├─ chat.py
│  │  │  ├─ plan.py
│  │  │  ├─ diff.py
│  │  │  ├─ apply.py
│  │  │  ├─ index.py
│  │  │  └─ search.py
│  │  ├─ core/
│  │  │  ├─ config.py
│  │  │  ├─ security.py
│  │  │  ├─ prompts.py
│  │  │  └─ logging.py
│  │  ├─ db/
│  │  │  ├─ session.py
│  │  │  ├─ models.py
│  │  │  └─ init_db.py
│  │  ├─ services/
│  │  │  ├─ ollama_client.py
│  │  │  ├─ context_builder.py
│  │  │  ├─ repo_indexer.py
│  │  │  ├─ search_service.py
│  │  │  ├─ patch_service.py
│  │  │  └─ task_service.py
│  │  ├─ schemas/
│  │  │  ├─ chat.py
│  │  │  ├─ diff.py
│  │  │  ├─ plan.py
│  │  │  ├─ search.py
│  │  │  └─ common.py
│  │  └─ utils/
│  │     ├─ fs.py
│  │     ├─ diff.py
│  │     └─ text.py
│  ├─ tests/
│  └─ alembic/
├─ editor-extension/
│  ├─ package.json
│  ├─ tsconfig.json
│  ├─ src/
│  │  ├─ extension.ts
│  │  ├─ api.ts
│  │  ├─ chatPanel.ts
│  │  ├─ diffView.ts
│  │  └─ commands.ts
│  └─ media/
├─ docs/
│  ├─ architecture.md
│  ├─ api.md
│  ├─ prompts.md
│  ├─ roadmap.md
│  └─ security.md
└─ scripts/
   ├─ run_backend.sh
   ├─ run_backend.ps1
   ├─ index_repo.py
   └─ setup_env.py
```

## Core API Contracts

### POST /chat
Request:
```json
{
  "project_id": "demo",
  "message": "Refactor the auth layer",
  "selected_files": ["backend/app/core/security.py"],
  "mode": "chat"
}
```

Response:
```json
{
  "reply": "...",
  "used_context": ["backend/app/core/security.py"],
  "tokens": 1234
}
```

### POST /plan
Request:
```json
{
  "project_id": "demo",
  "goal": "Add JWT refresh tokens"
}
```

Response:
```json
{
  "steps": [
    "Inspect current auth flow",
    "Add refresh token schema",
    "Update login endpoint",
    "Add tests"
  ]
}
```

### POST /diff
Request:
```json
{
  "project_id": "demo",
  "goal": "Add refresh tokens",
  "files": ["backend/app/core/security.py"]
}
```

Response:
```json
{
  "diff": "--- a/...\n+++ b/..."
}
```

### POST /apply
Request:
```json
{
  "project_id": "demo",
  "diff": "--- a/...\n+++ b/..."
}
```

Response:
```json
{
  "status": "applied"
}
```

### POST /index
Request:
```json
{
  "project_path": "/path/to/repo"
}
```

Response:
```json
{
  "status": "indexed",
  "files": 241
}
```

### POST /search
Request:
```json
{
  "project_id": "demo",
  "query": "authentication middleware"
}
```

Response:
```json
{
  "results": [
    {
      "path": "backend/app/core/security.py",
      "score": 0.91,
      "snippet": "..."
    }
  ]
}
```

## Backend Responsibilities

### main.py
- Create FastAPI app.
- Register routes.
- Add CORS if needed.
- Expose health endpoint.

### ollama_client.py
- Call local Ollama chat API.
- Support model selection.
- Handle retries and timeouts.

### context_builder.py
- Combine prompt, selected files, search hits, and repo metadata.
- Trim context to fit model limits.
- Rank snippets by relevance.

### repo_indexer.py
- Scan project files.
- Store file metadata.
- Extract chunks for search.
- Update index incrementally.

### search_service.py
- Run text search.
- Run semantic search if embeddings are enabled.
- Merge and rank results.

### patch_service.py
- Parse diff output.
- Validate patch structure.
- Apply or preview changes.
- Support rollback.

### task_service.py
- Store tasks and checkpoints.
- Track plans and outcomes.
- Keep lightweight session memory.

## Prompting Strategy
Use structured prompts with clear roles.

### System Prompt
- You are a code assistant.
- Prefer minimal, safe changes.
- Output diffs when asked to modify code.
- Never invent files.
- Ask clarifying questions when context is insufficient.

### Planner Prompt
- Break the task into steps.
- Keep each step small and reviewable.
- Mention risks and dependencies.

### Diff Prompt
- Output unified diff only.
- Do not add commentary.
- Preserve formatting.
- Touch only files in scope.

## Context Strategy
Use a layered context assembly approach.

1. User request.
2. Selected file content.
3. Nearby code chunks.
4. Search matches.
5. Project structure summary.
6. Previous session notes.

Keep the final prompt compact. Prefer the most relevant code instead of dumping large files.

## Local Model Setup
### Ollama model pull
```bash
ollama pull qwen2.5-coder:7b
```

### Example runtime call
```text
POST http://localhost:11434/api/chat
```

### Recommended generation settings
- temperature: 0.2
- top_p: 0.9
- max_tokens: task-dependent
- stop sequences: optional

## Environment Variables
```env
APP_NAME=ai-coding-assistant
APP_ENV=dev
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:7b
PROJECT_ROOT=/workspace/project
DATABASE_URL=sqlite:///./assistant.db
VECTOR_STORE_PATH=./data/vector_store
LOG_LEVEL=info
```

## Security Rules
- Require user approval before apply.
- Restrict shell commands to allowlisted actions.
- Never execute arbitrary prompts as code.
- Sanitize file paths.
- Log operations for auditability.
- Use separate workspaces for different projects.

## MVP Development Phases

### Phase 1: Backend skeleton
- Create FastAPI project.
- Add health check.
- Add Ollama client.
- Add config loading.

### Phase 2: Repo context
- Add file scanning.
- Add ripgrep search.
- Add context builder.
- Add project index endpoint.

### Phase 3: Chat and planning
- Implement chat endpoint.
- Implement task planning endpoint.
- Store sessions in SQLite.

### Phase 4: Diff generation
- Add diff schema.
- Generate and preview patches.
- Add apply/rollback support.

### Phase 5: Editor integration
- Build VS Code extension.
- Add chat panel.
- Add file selection and diff display.

### Phase 6: Polish
- Improve search quality.
- Add embeddings.
- Add history and checkpoints.
- Improve error handling.

## Acceptance Criteria
The MVP is complete when:
- A user can open a repo in the editor.
- The assistant can answer questions about code in the repo.
- The assistant can produce a correct patch for a small change.
- The user can review and apply the patch safely.
- The project can be re-indexed without manual cleanup.
- The system runs locally with Ollama and Qwen2.5-Coder.

## Example User Flow
1. Open the repo in the editor.
2. Ask: "Refactor the login flow to support refresh tokens."
3. Backend collects relevant files and search results.
4. Model generates a step plan.
5. User approves the plan.
6. Model generates a diff.
7. User reviews the diff in the editor.
8. User applies the change.
9. Tests are run manually or via an approved command.

## Notes for AI Editors
This project file is structured so an AI editor can scaffold code from it directly. The repo layout, API contracts, environment variables, and phase plan are intentionally explicit so the editor can generate the initial codebase from the markdown without needing extra design decisions.

## Suggested Next Files
- README.md with setup instructions.
- docs/architecture.md with diagrams.
- docs/api.md with request/response examples.
- docs/prompts.md with system and task prompts.
- backend/app/main.py with the FastAPI bootstrap.
- backend/app/services/ollama_client.py with model calls.
- editor-extension/src/extension.ts with command registration.