import type { ChatRequest } from "../types/chat";

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function streamChatMessage(
  request: ChatRequest,
  onChunk: (chunk: string) => void,
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/chat/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/plain",
    },
    body: JSON.stringify({
      ...request,
      stream: true,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      errorText || `Request failed with status ${response.status}`,
    );
  }

  if (!response.body) {
    throw new Error("Streaming is not supported by this browser.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      const chunk = decoder.decode(value, {
        stream: true,
      });

      if (chunk) {
        onChunk(chunk);
      }
    }
  } finally {
    reader.releaseLock();
  }
}