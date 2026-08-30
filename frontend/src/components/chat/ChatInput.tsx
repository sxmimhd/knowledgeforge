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

    if (!trimmedMessage || disabled) {
      return;
    }

    setMessage("");
    await onSend(trimmedMessage);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-zinc-800 bg-zinc-950 p-4"
    >
      <div className="mx-auto flex max-w-4xl gap-3">
        <input
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          disabled={disabled}
          placeholder="Message KnowledgeForge..."
          className="flex-1 rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-3 text-white outline-none placeholder:text-zinc-600 focus:border-zinc-600"
        />

        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="rounded-xl bg-white px-5 py-3 font-medium text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Send
        </button>
      </div>
    </form>
  );
}