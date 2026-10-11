
import { useState } from "react";

interface Props {
  onSend: (message: string) => Promise<void>;
  disabled?: boolean;
}

export default function ChatInput({
  onSend,
  disabled = false,
}: Props) {
  const [message, setMessage] = useState("");

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || disabled) return;

    setMessage("");
    await onSend(trimmedMessage);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-white/[0.08] bg-[#0c0c0f] px-6 py-5 max-sm:px-3"
    >
      <div className="mx-auto max-w-4xl">
        <div className="flex items-end gap-3 rounded-2xl border border-white/[0.1] bg-[#141418] p-2 transition focus-within:border-violet-400/40">
          <textarea
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            disabled={disabled}
            placeholder="Ask something about your knowledge…"
            rows={1}
            maxLength={12000}
            onKeyDown={(event) => {
              if (
                event.key === "Enter" &&
                !event.shiftKey &&
                !event.nativeEvent.isComposing
              ) {
                event.preventDefault();
                event.currentTarget.form?.requestSubmit();
              }
            }}
            className="max-h-36 min-h-11 flex-1 resize-y bg-transparent px-3 py-3 text-sm text-white outline-none placeholder:text-zinc-600 disabled:opacity-50"
          />

          <button
            type="submit"
            disabled={disabled || !message.trim()}
            className="mb-0.5 flex h-10 shrink-0 items-center gap-2 rounded-xl bg-violet-500 px-4 text-sm font-medium text-white transition hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-35"
          >
            {disabled ? (
              <>
                <span className="h-3 w-3 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                <span className="max-sm:hidden">Thinking</span>
              </>
            ) : (
              <>
                <span>Send</span>
                <span aria-hidden="true">↑</span>
              </>
            )}
          </button>
        </div>

        <p className="mt-3 text-center text-[10px] text-zinc-600">
          KnowledgeForge can make mistakes. Verify important information against your sources.
        </p>
      </div>
    </form>
  );
}
