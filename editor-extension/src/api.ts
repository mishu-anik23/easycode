import fetch from 'node-fetch';

const BASE_URL = 'http://127.0.0.1:8000';

export async function sendChatRequest(message: string) {
  const response = await fetch(`${BASE_URL}/chat/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ project_id: 'easycode', message, selected_files: [] }),
  });
  return await response.json();
}
