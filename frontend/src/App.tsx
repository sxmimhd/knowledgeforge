import { useState } from "react";

import ChatInput from "./components/chat/ChatInput";
import ChatWindow from "./components/chat/ChatWindow";
import { streamChatMessage } from "./services/api";
import type { ChatMessage } from "./types/chat";

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSend(message: string) {
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: message,
    };

    const assistantId = crypto.randomUUID();

    const assistantMessage: ChatMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
    };

    setMessages((current) => [
      ...current,
      userMessage,
      assistantMessage,
    ]);

    setLoading(true);

    try {
      await streamChatMessage(
        {
          message,
          system_prompt:
            "You are KnowledgeForge, a helpful AI assistant.",
          temperature: 0.7,
          top_p: 0.9,
          max_tokens: 500,
        },
        (chunk) => {
          setMessages((current) =>
            current.map((item) =>
              item.id === assistantId
                ? {
                    ...item,
                    content: item.content + chunk,
                  }
                : item,
            ),
          );
        },
      );
    } catch (error) {
      setMessages((current) =>
        current.map((item) =>
          item.id === assistantId
            ? {
                ...item,
                content:
                  error instanceof Error
                    ? `Error: ${error.message}`
                    : "An unexpected error occurred.",
              }
            : item,
        ),
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex h-screen flex-col bg-black">
      <header className="border-b border-zinc-800 px-6 py-4">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-white">
              KnowledgeForge
            </h1>

            <p className="text-xs text-zinc-500">
              LLM Playground
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs text-zinc-500">
            <span className="h-2 w-2 rounded-full bg-green-500" />
            Qwen · Ollama
          </div>
        </div>
      </header>

      <ChatWindow messages={messages} />

      {loading && (
        <div className="px-6 pb-2 text-center text-sm text-zinc-600">
          Qwen is thinking...
        </div>
      )}

      <ChatInput
        onSend={handleSend}
        disabled={loading}
      />
    </main>
  );
}

export default App;