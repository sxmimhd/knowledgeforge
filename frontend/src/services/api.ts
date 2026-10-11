
import type {
  KnowledgeDocument,
  SourceCitation,
} from "../types/chat";

export const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export const WORKSPACE_ID =
  "634c845b-ecb3-4055-a95b-3205b70f493d";

async function getError(response: Response): Promise<string> {
  const body = await response.text();

  if (!body) {
    return `Request failed (${response.status})`;
  }

  try {
    const parsed = JSON.parse(body);
    return (
      parsed.detail ??
      parsed.message ??
      parsed.error ??
      body
    );
  } catch {
    return body;
  }
}

async function requestJson<T>(
  url: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(url, init);

  if (!response.ok) {
    throw new Error(await getError(response));
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

function normalizeDocument(value: unknown): KnowledgeDocument {
  const item = value as Record<string, unknown>;

  return {
    ...item,
    id: String(item.id ?? item.document_id ?? ""),
    filename: String(
      item.filename ??
        item.file_name ??
        item.original_filename ??
        item.name ??
        "Untitled document",
    ),
    content_type:
      typeof item.content_type === "string"
        ? item.content_type
        : undefined,
    status:
      typeof item.status === "string"
        ? item.status
        : undefined,
    created_at:
      typeof item.created_at === "string"
        ? item.created_at
        : undefined,
  };
}

function extractDocuments(value: unknown): KnowledgeDocument[] {
  if (Array.isArray(value)) {
    return value.map(normalizeDocument);
  }

  if (value && typeof value === "object") {
    const object = value as Record<string, unknown>;

    for (const key of ["documents", "items", "results", "data"]) {
      if (Array.isArray(object[key])) {
        return (object[key] as unknown[]).map(normalizeDocument);
      }
    }
  }

  return [];
}

export async function listDocuments(): Promise<KnowledgeDocument[]> {
  const result = await requestJson<unknown>(
    `${API_BASE_URL}/workspaces/${WORKSPACE_ID}/documents`,
  );

  return extractDocuments(result);
}

export async function uploadDocument(
  file: File,
): Promise<unknown> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/workspaces/${WORKSPACE_ID}/documents`,
    {
      method: "POST",
      body: formData,
    },
  );

  if (!response.ok) {
    throw new Error(await getError(response));
  }

  const body = await response.text();
  return body ? JSON.parse(body) : null;
}

export async function deleteDocument(
  documentId: string,
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/workspaces/${WORKSPACE_ID}/documents/${encodeURIComponent(documentId)}`,
    { method: "DELETE" },
  );

  if (!response.ok) {
    throw new Error(await getError(response));
  }
}

function parseJsonIfPossible(value: string): unknown {
  try {
    return JSON.parse(value);
  } catch {
    return value;
  }
}

function extractSources(value: unknown): SourceCitation[] {
  const parsed =
    typeof value === "string" ? parseJsonIfPossible(value) : value;

  if (Array.isArray(parsed)) {
    return parsed as SourceCitation[];
  }

  if (parsed && typeof parsed === "object") {
    const object = parsed as Record<string, unknown>;

    if (Array.isArray(object.sources)) {
      return object.sources as SourceCitation[];
    }

    if (Array.isArray(object.citations)) {
      return object.citations as SourceCitation[];
    }

    if (Array.isArray(object.documents)) {
      return object.documents as SourceCitation[];
    }
  }

  return [];
}

function extractToken(value: string): string {
  const parsed = parseJsonIfPossible(value);

  if (typeof parsed === "string") {
    return parsed;
  }

  if (parsed && typeof parsed === "object") {
    const object = parsed as Record<string, unknown>;

    for (const key of ["token", "content", "text", "delta"]) {
      if (typeof object[key] === "string") {
        return object[key] as string;
      }

      if (
        object[key] &&
        typeof object[key] === "object"
      ) {
        const nested = object[key] as Record<string, unknown>;
        if (typeof nested.content === "string") {
          return nested.content;
        }
      }
    }
  }

  return "";
}

export async function streamRagMessage(
  query: string,
  onToken: (token: string) => void,
  onSources: (sources: SourceCitation[]) => void,
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/rag/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
    body: JSON.stringify({
      workspace_id: WORKSPACE_ID,
      query,
    }),
  });

  if (!response.ok) {
    throw new Error(await getError(response));
  }

  if (!response.body) {
    throw new Error("The browser could not read the response stream.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  function processEvent(block: string) {
    let eventName = "message";
    const dataLines: string[] = [];

    for (const line of block.split(/\r?\n/)) {
      if (line.startsWith("event:")) {
        eventName = line.slice(6).trim();
      } else if (line.startsWith("data:")) {
        dataLines.push(line.slice(5).trimStart());
      }
    }

    if (dataLines.length === 0) return;

    const data = dataLines.join("\n");

    if (eventName === "sources") {
      onSources(extractSources(data));
    } else if (eventName === "token" || eventName === "message") {
      const token = extractToken(data);
      if (token) onToken(token);
    }
  }

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      const blocks = buffer.split(/\r?\n\r?\n/);
      buffer = blocks.pop() ?? "";

      for (const block of blocks) {
        processEvent(block);
      }
    }

    buffer += decoder.decode();

    if (buffer.trim()) {
      processEvent(buffer);
    }
  } finally {
    reader.releaseLock();
  }
}
