
export type MessageRole = "user" | "assistant";

export interface SourceCitation {
  id?: string;
  title?: string;
  filename?: string;
  source?: string;
  document_name?: string;
  page?: number | string;
  page_number?: number | string;
  chunk_index?: number;
  content?: string;
  text?: string;
  score?: number;
  [key: string]: unknown;
}

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  sources?: SourceCitation[];
}

export interface ChatRequest {
  message: string;
  system_prompt: string;
  temperature: number;
  top_p: number;
  max_tokens: number;
  history?: ChatMessage[];
  stream?: boolean;
}

export interface KnowledgeDocument {
  id: string;
  filename: string;
  content_type?: string;
  status?: string;
  created_at?: string;
  [key: string]: unknown;
}
