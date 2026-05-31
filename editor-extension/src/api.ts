const BASE_URL = 'http://127.0.0.1:8000';

type ChatResponse = {
  reply: string;
  used_context: string[];
  tokens: number;
};

type SearchResponse = {
  results: string[];
};

type DiffResponse = {
  diff: string;
};

type ApplyResponse = {
  status: string;
};

async function request<T>(path: string, body: Record<string, unknown>): Promise<T> {
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
}

export async function sendChatRequest(message: string, selectedFiles: string[] = []): Promise<ChatResponse> {
  return request<ChatResponse>('/chat/', {
    project_id: 'easycode',
    message,
    selected_files: selectedFiles,
    mode: 'chat',
  });
}

export async function searchCode(query: string): Promise<string[]> {
  const response = await request<SearchResponse>('/search/', {
    project_id: 'easycode',
    query,
  });
  return response.results;
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
