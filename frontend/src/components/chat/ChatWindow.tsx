
import { useEffect, useRef } from "react";
import type { ChatMessage } from "../../types/chat";
import ChatMessageComponent from "./ChatMessage";

interface Props {
  messages: ChatMessage[];
}

export default function ChatWindow({ messages }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-1 flex-col overflow-y-auto px-6 py-8 max-sm:px-4">
      {messages.length === 0 ? (
        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xl text-center">
            <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl border border-violet-400/20 bg-violet-500/[0.08] text-3xl text-violet-300">
              ✳
            </div>

            <h2 className="text-3xl font-semibold tracking-tight text-white max-sm:text-2xl">
              Your knowledge, connected.
            </h2>

            <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-zinc-500">
              Ask questions about your documents. KnowledgeForge
              retrieves relevant information and streams an answer
              grounded in your workspace.
            </p>

            <div className="mt-8 grid grid-cols-2 gap-3 text-left max-sm:grid-cols-1">
              <div className="rounded-xl border border-white/[0.08] bg-white/[0.02] p-4">
                <span className="text-sm text-violet-300">01</span>
                <p className="mt-2 text-sm font-medium text-zinc-300">
                  Upload your knowledge
                </p>
                <p className="mt-1 text-xs leading-5 text-zinc-600">
                  Add PDFs, notes, and documentation in the sidebar.
                </p>
              </div>

              <div className="rounded-xl border border-white/[0.08] bg-white/[0.02] p-4">
                <span className="text-sm text-violet-300">02</span>
                <p className="mt-2 text-sm font-medium text-zinc-300">
                  Ask a grounded question
                </p>
                <p className="mt-1 text-xs leading-5 text-zinc-600">
                  Explore your material with retrieval-augmented AI.
                </p>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="mx-auto flex w-full max-w-4xl flex-col gap-6">
          {messages.map((message) => (
            <ChatMessageComponent
              key={message.id}
              message={message}
            />
          ))}
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
