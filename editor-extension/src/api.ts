const BASE_URL = 'http://127.0.0.1:8000';
const MAX_RETRIES = 3;
const RETRY_DELAY = 1000; // ms

type ChatResponse = {
  reply: string;
  used_context: string[];
  tokens: number;
};

type SearchResponse = {
  results: string[];
};

type SearchSourceResponse = {
  source: string;
  results: { path: string; name: string }[];
};

type DiffResponse = {
  diff: string;
};

type ApplyResponse = {
  status: string;
};

type FolderSearchResponse = {
  results: string[];
  source: string;
};

async function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function request<T>(path: string, body: Record<string, unknown>, retries: number = MAX_RETRIES): Promise<T> {
  if (typeof fetch === 'undefined') {
    throw new Error('The global fetch API is not available in this VS Code extension host.');
  }

  try {
    const response = await fetch(`${BASE_URL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`EasyCode backend error: ${response.status} ${text}`);
    }

    return response.json();
  } catch (error) {
    if (retries > 0 && error instanceof TypeError && error.message.includes('fetch')) {
      await delay(RETRY_DELAY);
      return request<T>(path, body, retries - 1);
    }

    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Cannot connect to EasyCode backend. Please ensure the backend server is running on http://127.0.0.1:8000');
    }

    throw error;
  }
}

export async function sendChatRequest(message: string, selectedFiles: string[] = []): Promise<ChatResponse> {
  return request<ChatResponse>('/chat/', {
    project_id: 'easycode',
    message,
    selected_files: selectedFiles,
    mode: 'chat',
  });
}

export async function searchCode(query: string, searchSource: string = 'local'): Promise<string[]> {
  const response = await request<SearchResponse>('/search/', {
    project_id: 'easycode',
    query,
    search_source: searchSource,
  });
  return response.results;
}

export async function searchFolderLocal(folderPath: string, query: string): Promise<string[]> {
  const response = await request<FolderSearchResponse>('/search/folder/local', {
    project_id: 'easycode',
    folder_path: folderPath,
    query,
  });
  return response.results;
}

export async function searchFolderGoogleDrive(query: string, authToken: string): Promise<string[]> {
  const response = await request<FolderSearchResponse>('/search/folder/google-drive', {
    project_id: 'easycode',
    query,
    auth_token: authToken,
  });
  return response.results;
}

export async function searchFolderDropbox(query: string, authToken: string): Promise<string[]> {
  const response = await request<FolderSearchResponse>('/search/folder/dropbox', {
    project_id: 'easycode',
    query,
    auth_token: authToken,
  });
  return response.results;
}

export async function getGoogleDriveAuthUrl(): Promise<{ auth_url: string }> {
  return request<{ auth_url: string }>('/auth/google-drive/url', {
    project_id: 'easycode',
  });
}

export async function getDropboxAuthUrl(): Promise<{ auth_url: string }> {
  return request<{ auth_url: string }>('/auth/dropbox/url', {
    project_id: 'easycode',
  });
}

export async function generateDiff(goal: string, files: string[]): Promise<DiffResponse> {
  return request<DiffResponse>('/diff/', {
    project_id: 'easycode',
    goal,
    files,
  });
}

export async function applyDiff(diff: string): Promise<ApplyResponse> {
  return request<ApplyResponse>('/apply/', {
    project_id: 'easycode',
    diff,
  });
}
