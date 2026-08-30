export type MessageRole = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
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