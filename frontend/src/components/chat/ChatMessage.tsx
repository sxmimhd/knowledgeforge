
import type {
  ChatMessage as ChatMessageType,
  SourceCitation,
} from "../../types/chat";

interface Props {
  message: ChatMessageType;
}

function getSourceName(source: SourceCitation): string {
  return (
    source.filename ??
    source.document_name ??
    source.title ??
    source.source ??
    "Retrieved document"
  );
}

function getSourceDetail(source: SourceCitation): string {
  const page = source.page ?? source.page_number;

  if (page !== undefined && page !== null && page !== "") {
    return `Page ${page}`;
  }

  if (typeof source.chunk_index === "number") {
    return `Chunk ${source.chunk_index}`;
  }

  return "";
}

export default function ChatMessage({ message }: Props) {
  const isUser = message.role === "user";
  const sources = message.sources ?? [];

  return (
    <div
      className={`flex w-full ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div className="max-w-3xl min-w-0">
        <div
          className={`rounded-2xl px-4 py-3 ${
            isUser
              ? "bg-zinc-100 text-zinc-950"
              : "border border-white/[0.08] bg-[#111114] text-zinc-100"
          }`}
        >
          <div className="mb-2 text-[10px] font-semibold uppercase tracking-[0.14em] opacity-50">
            {isUser ? "You" : "KnowledgeForge"}
          </div>

          <p className="whitespace-pre-wrap break-words text-sm leading-7">
            {message.content ||
              (isUser ? "" : "Preparing your answer…")}
          </p>
        </div>

        {!isUser && sources.length > 0 && (
          <div className="mt-3">
            <p className="mb-2 text-[10px] font-semibold uppercase tracking-[0.14em] text-zinc-500">
              Sources · {sources.length}
            </p>

            <div className="flex flex-wrap gap-2">
              {sources.map((source, index) => {
                const name = getSourceName(source);
                const detail = getSourceDetail(source);
                const key =
                  source.id ??
                  `${name}-${detail}-${index}`;

                const excerpt =
                  source.content ?? source.text;

                return (
                  <details
                    key={key}
                    className="group max-w-full rounded-xl border border-white/[0.09] bg-white/[0.025] text-xs"
                  >
                    <summary className="flex cursor-pointer list-none items-center gap-2 px-3 py-2.5 text-zinc-300 hover:text-white">
                      <span className="text-violet-300">▤</span>
                      <span className="max-w-[240px] truncate">
                        {name}
                      </span>
                      {detail && (
                        <span className="shrink-0 text-zinc-600">
                          {detail}
                        </span>
                      )}
                      <span className="ml-1 text-zinc-600 transition group-open:rotate-180">
                        ⌄
                      </span>
                    </summary>

                    {typeof excerpt === "string" && excerpt && (
                      <div className="max-w-xl border-t border-white/[0.07] px-3 py-3 leading-6 text-zinc-400">
                        {excerpt}
                      </div>
                    )}
                  </details>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
