
import { useCallback, useEffect, useRef, useState } from "react";

import ChatInput from "./components/chat/ChatInput";
import ChatWindow from "./components/chat/ChatWindow";
import {
  deleteDocument,
  listDocuments,
  streamRagMessage,
  uploadDocument,
  WORKSPACE_ID,
} from "./services/api";
import type {
  ChatMessage,
  KnowledgeDocument,
  SourceCitation,
} from "./types/chat";

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [documents, setDocuments] = useState<KnowledgeDocument[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const refreshDocuments = useCallback(async () => {
    setLoadingDocuments(true);

    try {
      const result = await listDocuments();
      setDocuments(result);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not load your documents.",
      );
    } finally {
      setLoadingDocuments(false);
    }
  }, []);

  useEffect(() => {
    void refreshDocuments();
  }, [refreshDocuments]);

  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    const files = Array.from(event.target.files ?? []);
    event.target.value = "";

    if (!files.length) return;

    setError("");
    setNotice("");
    setUploading(true);

    const failedFiles: string[] = [];
    let uploadedCount = 0;

    try {
      for (const file of files) {
        try {
          await uploadDocument(file);
          uploadedCount += 1;
        } catch (err) {
          failedFiles.push(
            `${file.name}: ${
              err instanceof Error ? err.message : "Upload failed"
            }`,
          );
        }
      }

      if (uploadedCount > 0) {
        setNotice(
          `${uploadedCount} document${uploadedCount === 1 ? "" : "s"} uploaded successfully.`,
        );
        await refreshDocuments();
      }

      if (failedFiles.length > 0) {
        setError(failedFiles.join("\n"));
      }
    } finally {
      setUploading(false);
    }
  }

  async function handleDelete(document: KnowledgeDocument) {
    if (!document.id) {
      setError("This document has no ID, so it cannot be deleted.");
      return;
    }

    const confirmed = window.confirm(
      `Delete "${document.filename}" from this workspace?`,
    );

    if (!confirmed) return;

    setError("");
    setNotice("");
    setDeletingId(document.id);

    try {
      await deleteDocument(document.id);
      setDocuments((current) =>
        current.filter((item) => item.id !== document.id),
      );
      setNotice(`Deleted "${document.filename}".`);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not delete the document.",
      );
    } finally {
      setDeletingId(null);
    }
  }

  async function handleSend(query: string) {
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: query,
    };

    const assistantId = crypto.randomUUID();

    const assistantMessage: ChatMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
      sources: [],
    };

    setMessages((current) => [
      ...current,
      userMessage,
      assistantMessage,
    ]);

    setLoading(true);
    setError("");
    setNotice("");

    try {
      await streamRagMessage(
        query,
        (token) => {
          setMessages((current) =>
            current.map((message) =>
              message.id === assistantId
                ? {
                    ...message,
                    content: message.content + token,
                  }
                : message,
            ),
          );
        },
        (sources: SourceCitation[]) => {
          setMessages((current) =>
            current.map((message) =>
              message.id === assistantId
                ? { ...message, sources }
                : message,
            ),
          );
        },
      );
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "An unexpected error occurred.";

      setMessages((current) =>
        current.map((item) =>
          item.id === assistantId
            ? {
                ...item,
                content: item.content
                  ? `${item.content}\n\n[Stream interrupted: ${message}]`
                  : `I couldn't complete that request: ${message}`,
              }
            : item,
        ),
      );
    } finally {
      setLoading(false);
    }
  }

  function formatFileSize(value: unknown): string {
    if (typeof value !== "number" || value < 0) return "";

    if (value < 1024) return `${value} B`;
    if (value < 1024 * 1024) {
      return `${(value / 1024).toFixed(1)} KB`;
    }

    return `${(value / (1024 * 1024)).toFixed(1)} MB`;
  }

  return (
    <main className="flex h-dvh overflow-hidden bg-[#09090b] text-zinc-100">
      <aside className="flex w-[300px] shrink-0 flex-col border-r border-white/[0.08] bg-[#0c0c0f] max-md:w-[220px] max-sm:w-[76px]">
        <div className="border-b border-white/[0.08] px-5 py-5 max-sm:px-3">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-violet-500/15 text-lg font-bold text-violet-300 ring-1 ring-violet-400/20">
              K
            </div>
            <div className="min-w-0 max-sm:hidden">
              <h1 className="font-semibold tracking-tight">
                KnowledgeForge
              </h1>
              <p className="mt-0.5 text-xs text-zinc-500">
                Knowledge workspace
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between px-4 pb-3 pt-5 max-sm:justify-center max-sm:px-2">
          <div className="max-sm:hidden">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">
              Your knowledge
            </p>
            <p className="mt-1 text-xs text-zinc-600">
              {documents.length} document{documents.length === 1 ? "" : "s"}
            </p>
          </div>

          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
            title="Upload documents"
            className="flex items-center gap-2 rounded-lg bg-violet-500 px-3 py-2 text-sm font-medium text-white transition hover:bg-violet-400 disabled:opacity-50 max-sm:px-2"
          >
            <span className="text-lg leading-none">+</span>
            <span className="max-sm:hidden">
              {uploading ? "Uploading…" : "Add files"}
            </span>
          </button>

          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".pdf,.md,.markdown,.txt,.csv,.json"
            onChange={handleUpload}
            className="hidden"
          />
        </div>

        <div className="flex-1 overflow-y-auto px-3 pb-4">
          {loadingDocuments ? (
            <p className="px-3 py-6 text-sm text-zinc-500 max-sm:hidden">
              Loading documents…
            </p>
          ) : documents.length === 0 ? (
            <div className="mx-2 mt-3 rounded-xl border border-dashed border-white/10 px-4 py-6 text-center max-sm:hidden">
              <div className="mx-auto mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-white/[0.04] text-xl">
                <span>↥</span>
              </div>
              <p className="text-sm font-medium text-zinc-300">
                No documents yet
              </p>
              <p className="mt-2 text-xs leading-5 text-zinc-500">
                Upload files to give your AI a knowledge base to search.
              </p>
            </div>
          ) : (
            <div className="space-y-1">
              {documents.map((document) => {
                const extension =
                  document.filename.split(".").pop()?.toUpperCase() ??
                  "FILE";

                const fileSize = formatFileSize(document.size);

                return (
                  <div
                    key={document.id || document.filename}
                    className="group flex items-center gap-3 rounded-xl px-3 py-3 transition hover:bg-white/[0.04] max-sm:justify-center max-sm:px-1"
                    title={document.filename}
                  >
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-white/[0.07] bg-white/[0.03] text-[9px] font-bold text-violet-300">
                      {extension.slice(0, 4)}
                    </div>

                    <div className="min-w-0 flex-1 max-sm:hidden">
                      <p className="truncate text-sm text-zinc-300">
                        {document.filename}
                      </p>
                      <p className="mt-1 truncate text-xs text-zinc-600">
                        {document.status ?? "Added"}
                        {fileSize ? ` · ${fileSize}` : ""}
                      </p>
                    </div>

                    <button
                      type="button"
                      onClick={() => void handleDelete(document)}
                      disabled={deletingId === document.id}
                      title={`Delete ${document.filename}`}
                      aria-label={`Delete ${document.filename}`}
                      className="rounded-md px-2 py-1 text-sm text-zinc-600 opacity-0 transition hover:bg-red-500/10 hover:text-red-400 group-hover:opacity-100 focus:opacity-100 max-sm:hidden"
                    >
                      {deletingId === document.id ? "…" : "×"}
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="border-t border-white/[0.08] p-4 max-sm:px-2">
          <div className="rounded-xl bg-white/[0.03] p-3 max-sm:flex max-sm:justify-center max-sm:p-2">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              <span className="text-xs text-zinc-400 max-sm:hidden">
                Local AI · Ollama
              </span>
            </div>
            <p className="mt-2 break-all font-mono text-[10px] text-zinc-600 max-sm:hidden">
              Workspace {WORKSPACE_ID.slice(0, 8)}…
            </p>
          </div>
        </div>
      </aside>

      <section className="flex min-w-0 flex-1 flex-col">
        <header className="flex min-h-[73px] items-center justify-between border-b border-white/[0.08] px-6 py-4 max-sm:px-4">
          <div>
            <h2 className="font-medium text-zinc-100">
              Knowledge chat
            </h2>
            <p className="mt-1 text-xs text-zinc-500">
              Ask questions about your uploaded documents
            </p>
          </div>

          <button
            type="button"
            onClick={() => {
              setMessages([]);
              setError("");
              setNotice("");
            }}
            className="rounded-lg border border-white/10 px-3 py-2 text-xs text-zinc-400 transition hover:bg-white/[0.05] hover:text-white"
          >
            New chat
          </button>
        </header>

        {(error || notice) && (
          <div className="space-y-2 px-6 pt-4 max-sm:px-3">
            {error && (
              <div
                role="alert"
                className="whitespace-pre-wrap rounded-xl border border-red-500/20 bg-red-500/[0.07] px-4 py-3 text-sm text-red-300"
              >
                {error}
                <button
                  type="button"
                  onClick={() => setError("")}
                  className="float-right ml-3 text-red-200"
                  aria-label="Dismiss error"
                >
                  ×
                </button>
              </div>
            )}
            {notice && (
              <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/[0.06] px-4 py-3 text-sm text-emerald-300">
                {notice}
              </div>
            )}
          </div>
        )}

        <ChatWindow messages={messages} />

        {loading && (
          <div className="px-6 pb-3 text-xs text-violet-300/80 max-sm:px-4">
            <span className="mr-2 inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-violet-400" />
            Searching your knowledge and generating an answer…
          </div>
        )}

        <ChatInput onSend={handleSend} disabled={loading} />
      </section>
    </main>
  );
}

export default App;
