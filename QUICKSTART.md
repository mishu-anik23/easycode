# EasyCode Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Install Dependencies

```powershell
# Clone repository
git clone https://github.com/mishu-anik23/easycode.git
cd easycode

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r backend/requirements.txt

# Install extension dependencies
cd editor-extension
npm install
cd ..
```

### 2. Start Ollama (for AI features)

```powershell
# In a new terminal, start Ollama service
ollama serve

# In another terminal, pull a model (one-time)
ollama pull mistral
```

### 3. Start Backend

```powershell
# From repository root (with virtual env active)
python -m uvicorn backend.app.main:app --reload --port 8000
```

### 4. Start Extension

```powershell
# In VS Code, open editor-extension folder
# Press F5 to launch extension
```

## 📋 Available Commands

After launching extension, use Command Palette (Ctrl+Shift+P) to run:

### `EasyCode: Start Chat`
Chat with AI assistant about your code
- Optionally select a file for context
- Get AI insights and suggestions

### `EasyCode: Search Codebase`
Search in current repository
- Fast code search
- Returns matching lines with line numbers

### `EasyCode: Search Folders (Local/Google Drive/Dropbox)` ⭐ NEW
Search across different storage sources:
- **Local**: Browse and search any folder
- **Google Drive**: Search your Google Drive files
- **Dropbox**: Search your Dropbox files

### `EasyCode: Generate Diff`
AI generates code changes based on description
- Describe what you want to change
- AI creates unified diff
- Review before applying

### `EasyCode: Apply Diff`
Apply generated diffs to files
- Paste diff or select from file
- Automatically applies changes
- Creates backup before modifying

## 🐛 Troubleshooting

### Error: "Cannot connect to EasyCode backend"
```
✓ Backend not running? Start it:
  python -m uvicorn backend.app.main:app --reload --port 8000

✓ Wrong port? Ensure backend is on port 8000

✓ Firewall issue? Allow localhost:8000
```

### Error: Chat doesn't work
```
✓ Is Ollama running? Start with: ollama serve

✓ Model installed? Check with: ollama pull mistral

✓ Check logs in Output panel (select "EasyCode" channel)
```

### Extension won't load
```
✓ Rebuild: npm run compile

✓ Clear cache: Delete .vscode/extensions folder

✓ Reload VS Code window: Ctrl+Shift+P → Reload Window
```

## 🌐 Cloud Storage Setup (Optional)

### Google Drive
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create project and enable Google Drive API
3. Create OAuth2 credentials
4. Add to `.env`:
```
GOOGLE_DRIVE_CLIENT_ID=your_client_id
GOOGLE_DRIVE_CLIENT_SECRET=your_secret
```

### Dropbox
1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Create new app
3. Get app key and secret
4. Add to `.env`:
```
DROPBOX_APP_KEY=your_app_key
DROPBOX_APP_SECRET=your_secret
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

## 📚 Useful Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+P` | Open Command Palette |
| `Ctrl+Shift+U` | Open Output channel |
| `F5` (in editor-extension) | Launch extension |
| `Ctrl+Shift+D` | Debug panel |

## 📖 Learn More

- [README.md](README.md) - Feature overview
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Error solutions
- [docs/API_ENDPOINTS.md](docs/API_ENDPOINTS.md) - API reference

## 🎓 Common Workflows

### Workflow 1: Understand Code
```
1. Open file in editor
2. Select code
3. Command: EasyCode: Start Chat
4. Ask "What does this do?"
5. Get AI explanation
```

### Workflow 2: Search for Similar Code
```
1. Command: EasyCode: Search Codebase
2. Enter search term
3. Browse results
4. Click to navigate
```

### Workflow 3: Search Cloud Storage
```
1. Command: EasyCode: Search Folders
2. Select source (Local/Google Drive/Dropbox)
3. Choose folder (for local) or authenticate
4. Enter search query
5. Browse results
```

### Workflow 4: Generate Changes
```
1. Command: EasyCode: Generate Diff
2. Describe desired changes
3. Review generated diff
4. Command: EasyCode: Apply Diff
5. Changes applied to files
```

## 🔗 Resources

- [VS Code Extension API](https://code.visualstudio.com/api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ollama Official Site](https://ollama.ai)

## ❓ FAQ

**Q: Can I use this with projects other than Python?**
A: Yes! The search supports multiple languages (.js, .ts, .java, .go, .cpp, etc.)

**Q: Does cloud storage search cost money?**
A: Google Drive and Dropbox integration is free using your own credentials.

**Q: Can I use this without Ollama?**
A: You need Ollama for chat features, but search works without it.

**Q: Is data stored anywhere?**
A: Everything runs locally. No data is sent to external servers except cloud storage searches (which go to your Google Drive or Dropbox).

**Q: How do I uninstall?**
A: Extension can be disabled in VS Code. Delete folder to fully uninstall.

## 🚀 Next Steps

1. ✅ Complete setup above
2. ✅ Try each command once
3. ✅ Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for configuration
4. ✅ Check [docs/API_ENDPOINTS.md](docs/API_ENDPOINTS.md) for advanced features
5. ✅ Enjoy coding with AI assistance!

## 📝 Version Info

- Current: v0.2.0
- Backend: FastAPI
- Extension: VS Code 1.80+
- Requirements: Python 3.8+, Node.js 14+

---

**Questions?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or [SETUP_GUIDE.md](SETUP_GUIDE.md)
