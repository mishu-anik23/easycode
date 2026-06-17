# EasyCode Troubleshooting Guide

## Error: "Cannot connect to EasyCode backend"

### Symptoms
- "fetch failed" error when running `EasyCode: Start Chat`
- Extension shows error: "Cannot connect to EasyCode backend. Please ensure the backend server is running on http://127.0.0.1:8000"

### Common Causes & Solutions

#### 1. Backend Server Not Running
**Check:**
```powershell
# Verify backend is running by opening this in browser
http://127.0.0.1:8000/
# Should return: {"status": "EasyCode backend is running"}
```

**Fix:**
```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

#### 2. Wrong Port Configuration
**Check:** Ensure both extension and backend use port 8000
- Backend: `http://127.0.0.1:8000`
- Extension: `const BASE_URL = 'http://127.0.0.1:8000'` in [editor-extension/src/api.ts](editor-extension/src/api.ts)

#### 3. Firewall Blocking Connection
**Fix:** Add localhost exception or use WSL with firewall disabled for development

#### 4. Backend Crashes on Startup
**Check terminal output for:**
- Missing dependencies
- Import errors
- Configuration issues

**Fix:**
```powershell
# Reinstall dependencies
pip install -r backend/requirements.txt --force-reinstall
```

#### 5. Ollama Service Not Running
**Check:** Ollama needs to be running for chat functionality
```powershell
# In separate terminal, start Ollama
ollama serve

# In another terminal, verify with:
curl http://localhost:11434/api/tags
```

**Fix:** Download and install Ollama from [ollama.ai](https://ollama.ai)

### Debugging Steps

1. **Check Backend Logs**
   ```powershell
   # Terminal where backend is running should show requests and errors
   ```

2. **Enable Extension Debug Output**
   - Open VS Code Output panel
   - Select "EasyCode" channel
   - Run the command again

3. **Test API Directly**
   ```powershell
   # Test chat endpoint
   curl -X POST http://127.0.0.1:8000/chat/ `
     -H "Content-Type: application/json" `
     -d '{
       "project_id": "easycode",
       "message": "Hello",
       "selected_files": [],
       "mode": "chat"
     }'
   ```

4. **Check Network**
   ```powershell
   # Verify localhost is accessible
   ping 127.0.0.1
   
   # Check port is listening
   netstat -an | findstr :8000
   ```

## Error: "Failed to authenticate with Google Drive/Dropbox"

### Solutions
1. Verify OAuth credentials in `.env` file
2. Check redirect URIs match exactly in OAuth console
3. Ensure client ID and client secret are correct
4. See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed OAuth setup

## Error: "No matches found" in Search

### Possible Issues
1. Query might be too specific
2. Files not indexed yet (for cloud storage)
3. File types not supported
4. Permission issues accessing files

### Fix
- Try simpler search terms
- Verify files exist in selected folder
- Check file permissions
- For cloud storage, ensure you're authenticated

## Performance Issues

### Slow Search Results
- Results are limited to first 50 matches
- Cloud storage searches may be slower
- Try more specific queries

### Extension Freezes
- Backend may be processing large requests
- Check terminal for long-running operations
- Restart extension if needed (Reload Window)

## Debug Commands

```powershell
# View backend logs in real-time
Get-Content -Path "backend.log" -Tail 10 -Wait

# Test network connectivity to backend
Test-NetConnection -ComputerName 127.0.0.1 -Port 8000

# Check Python version and packages
python --version
pip list
```

## Getting More Help

1. Check extension output channel for detailed error messages
2. Enable debug logging in [editor-extension/src/extension.ts](editor-extension/src/extension.ts)
3. Check backend logs at startup
4. Verify all dependencies are installed correctly
5. Try restarting both backend and extension
