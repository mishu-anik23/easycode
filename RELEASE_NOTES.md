# EasyCode v0.2.0 - Release Notes

## 🎯 Summary of Changes

This release fixes the "fetch failed" error and adds comprehensive folder search functionality with cloud storage integration.

## 🔧 Bug Fixes

### Fixed: "Cannot connect to EasyCode backend" Error
- **Issue**: Extension was failing with "fetch failed" when backend wasn't available
- **Solution**: 
  - Added automatic retry logic (3 retries with 1-second delays)
  - Implemented better error handling and user-friendly error messages
  - Added clear instructions for users when backend is unavailable
  - Error now shows: "Cannot connect to EasyCode backend. Please ensure the backend server is running on http://127.0.0.1:8000"

**Files Modified:**
- [editor-extension/src/api.ts](editor-extension/src/api.ts) - Added retry mechanism and improved error handling

## ✨ New Features

### 1. Multi-Source Folder Search
Users can now search for code across different storage sources:

#### Local Folder Search
- Browse and select any folder on local machine
- Search through common code file types (.py, .js, .ts, .java, .cpp, .go, .rs, etc.)
- Results include file path and line number

#### Google Drive Integration
- OAuth2 authentication support
- Search for code files by name and content
- Direct links to files in Google Drive

#### Dropbox Integration
- OAuth2 authentication support
- Search for code files in Dropbox
- Get direct Dropbox file paths

**New Command:**
- `EasyCode: Search Folders (Local/Google Drive/Dropbox)` - Access all three search sources

### 2. Cloud Storage Authentication
New authentication endpoints for OAuth2 integration:
- `POST /auth/google-drive/url` - Get Google Drive auth URL
- `POST /auth/dropbox/url` - Get Dropbox auth URL
- `GET /auth/google-drive/callback` - Handle Google Drive callback
- `GET /auth/dropbox/callback` - Handle Dropbox callback

### 3. Enhanced Search API
New backend endpoints for folder-based searches:
- `POST /search/folder/local` - Search in local folder
- `POST /search/folder/google-drive` - Search in Google Drive
- `POST /search/folder/dropbox` - Search in Dropbox

## 📁 Files Added

### Backend
- [backend/app/services/cloud_search_service.py](backend/app/services/cloud_search_service.py) - Cloud storage integration
- [backend/app/api/auth.py](backend/app/api/auth.py) - OAuth2 authentication endpoints

### Documentation
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Comprehensive setup instructions
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Troubleshooting guide for common errors
- [docs/API_ENDPOINTS.md](docs/API_ENDPOINTS.md) - Complete API endpoint documentation

## 📝 Files Modified

### Backend
- [backend/app/main.py](backend/app/main.py) - Added auth router
- [backend/app/api/search.py](backend/app/api/search.py) - Added new search endpoints
- [backend/app/schemas/search.py](backend/app/schemas/search.py) - Added new request/response schemas
- [backend/app/services/search_service.py](backend/app/services/search_service.py) - Added folder search method

### Extension
- [editor-extension/src/api.ts](editor-extension/src/api.ts) - Added retry logic, cloud storage API functions
- [editor-extension/src/extension.ts](editor-extension/src/extension.ts) - Added folder search command handler
- [editor-extension/package.json](editor-extension/package.json) - Added new command registration

### Documentation
- [README.md](README.md) - Updated with new features
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - New comprehensive setup guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - New troubleshooting documentation

## 🚀 How to Use New Features

### Local Folder Search
1. Run command: `EasyCode: Search Folders (Local/Google Drive/Dropbox)`
2. Select "Local Folder"
3. Choose folder to search
4. Enter search query
5. View results

### Google Drive Search
1. Run command: `EasyCode: Search Folders (Local/Google Drive/Dropbox)`
2. Select "Google Drive"
3. Authenticate if prompted
4. Enter search query
5. View results with direct links

### Dropbox Search
1. Run command: `EasyCode: Search Folders (Local/Google Drive/Dropbox)`
2. Select "Dropbox"
3. Authenticate if prompted
4. Enter search query
5. View results with Dropbox paths

## 🔐 Configuration

Cloud storage requires OAuth2 setup. See [SETUP_GUIDE.md](SETUP_GUIDE.md) for:
- Google Drive OAuth2 configuration
- Dropbox OAuth2 configuration
- Environment variable setup

## ⚙️ Technical Details

### Error Handling
- Automatic retry mechanism (3 attempts)
- 1-second delay between retries
- Graceful fallback with user-friendly messages

### API Changes
All new search endpoints follow the same pattern:
```json
{
  "project_id": "easycode",
  "query": "search_term",
  "folder_path": "/path/to/folder",  // for local searches
  "auth_token": "oauth_token"        // for cloud searches
}
```

### Supported File Types
Local and cloud searches support:
- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- C/C++ (.cpp, .c)
- Go (.go)
- Rust (.rs)
- Ruby (.rb)

## 🧪 Testing

### Backend Testing
```bash
# Test new search endpoints
pytest backend/tests/

# Test API with curl
curl -X POST http://127.0.0.1:8000/search/folder/local \
  -H "Content-Type: application/json" \
  -d '{"project_id": "easycode", "folder_path": "/path", "query": "test"}'
```

### Extension Testing
1. Build: `npm run compile`
2. Launch with F5 in VS Code
3. Test new command via Command Palette

## 📚 Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Complete setup instructions
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Error resolution guide
- [docs/API_ENDPOINTS.md](docs/API_ENDPOINTS.md) - Full API reference
- [README.md](README.md) - Feature overview

## 🔮 Future Enhancements

- [ ] Real-time file indexing for cloud storage
- [ ] Search result caching
- [ ] Advanced filtering options
- [ ] Batch operations support
- [ ] WebSocket support for real-time updates
- [ ] More cloud storage providers (Microsoft OneDrive, AWS S3)

## ⚠️ Known Limitations

- Google Drive and Dropbox authentication tokens must be manually entered (OAuth callback not yet implemented in UI)
- Cloud storage searches are limited to first 50 results
- File content search for cloud storage requires specific API permissions

## 📞 Support

For issues or questions:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review [SETUP_GUIDE.md](SETUP_GUIDE.md) for configuration
3. Check [docs/API_ENDPOINTS.md](docs/API_ENDPOINTS.md) for API details

## 🙏 Credits

Built with:
- FastAPI (backend)
- VS Code Extension API
- OAuth2 for cloud storage integration
- Ollama for local LLM
