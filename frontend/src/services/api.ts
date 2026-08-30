import type { ChatRequest } from "../types/chat";

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function sendChatMessage(
  request: ChatRequest,
): Promise<string> {
  const params = new URLSearchParams({
    message: request.message,
  });

  const response = await fetch(
    `${API_BASE_URL}/chat/?${params.toString()}`,
    {
      method: "POST",
      headers: {
        Accept: "application/json",
      },
    },
  );

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      errorText || `Request failed with status ${response.status}`,
    );
  }

  const result = await response.json();

  return result.data.response;
}