import type { ChatMessage } from "../../types/chat";
import ChatMessageComponent from "./ChatMessage";

interface Props {
  messages: ChatMessage[];
}

export default function ChatWindow({ messages }: Props) {
  return (
    <div className="flex flex-1 flex-col gap-4 overflow-y-auto px-6 py-8">
      {messages.length === 0 ? (
        <div className="flex flex-1 items-center justify-center">
          <div className="text-center">
            <h2 className="text-3xl font-semibold text-white">
              KnowledgeForge
            </h2>

            <p className="mt-3 text-zinc-500">
              Ask anything to test the LLM Playground.
            </p>
          </div>
        </div>
      ) : (
        messages.map((message) => (
          <ChatMessageComponent
            key={message.id}
            message={message}
          />
        ))
      )}
    </div>
  );
}