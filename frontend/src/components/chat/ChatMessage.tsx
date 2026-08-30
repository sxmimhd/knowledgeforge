import type { ChatMessage as ChatMessageType } from "../../types/chat";

interface Props {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex w-full ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-3xl rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-white text-black"
            : "bg-zinc-900 text-zinc-100 border border-zinc-800"
        }`}
      >
        <p className="whitespace-pre-wrap leading-7">
          {message.content}
        </p>
      </div>
    </div>
  );
}