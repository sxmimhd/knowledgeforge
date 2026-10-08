from typing import Any

from app.services.llm.dependencies import get_llm
from app.services.retrieval.retrieval import RetrievalService


class RAGService:
    def __init__(
        self,
        retrieval: RetrievalService | None = None,
        llm=None,
    ):
        self.retrieval = retrieval or RetrievalService()
        self.llm = llm or get_llm()

    def _build_prompt(
        self,
        query: str,
        context: str,
    ) -> list[dict[str, str]]:
        system_prompt = """You are KnowledgeForge, an enterprise knowledge assistant.

Answer the user's question using ONLY the provided knowledge context.

Rules:
- Do not invent facts.
- Do not use outside knowledge.
- If the answer cannot be found in the context, say that the information was not found in the provided knowledge base.
- Be concise and directly answer the question.
- Every factual statement based on the knowledge context MUST include one or more citations.
- Use the exact citation format [1], [2], [3], etc.
- Only cite sources that actually support the statement.
- Do not create citation numbers that do not exist.
- Put citations immediately after the relevant statement.

Knowledge Context:
------------------
{context}
------------------
""".format(context=context)

        return [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": query,
            },
        ]

    def _prepare(
        self,
        query: str,
        top_k: int,
        metadata_filter: dict[str, Any] | None,
    ):
        results = self.retrieval.retrieve(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )

        context_parts = []

        sources = []

        for index, result in enumerate(results, start=1):
            metadata = result.get("metadata", {})

            filename = metadata.get(
                "filename",
                metadata.get("source", "unknown"),
            )

            context_parts.append(
                f"[{index}] Source: {filename}\n"
                f"Chunk: {metadata.get('chunk_index', 'unknown')}\n"
                f"{result.get('text', '')}"
            )

            sources.append(
                {
                    "id": index,
                    "filename": metadata.get("filename"),
                    "source": metadata.get("source"),
                    "chunk_index": metadata.get("chunk_index"),
                    "score": result.get("score"),
                }
            )

        if context_parts:
            context = "\n\n".join(context_parts)
        else:
            context = "No relevant information was found."

        messages = self._build_prompt(
            query=query,
            context=context,
        )

        return results, messages, sources

    async def generate(
        self,
        query: str,
        top_k: int = 5,
        metadata_filter: dict[str, Any] | None = None,
        temperature: float = 0.2,
        max_tokens: int = 500,
    ) -> dict[str, Any]:

        results, messages, sources = self._prepare(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )

        answer = await self.llm.generate(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return {
            "answer": answer,
            "sources": sources,
            "retrieved_chunks": len(results),
        }

    async def stream(
        self,
        query: str,
        top_k: int = 5,
        metadata_filter: dict[str, Any] | None = None,
        temperature: float = 0.2,
        max_tokens: int = 500,
    ):
        results, messages, sources = self._prepare(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )

        async for token in self.llm.stream(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            yield token

    async def stream_with_sources(
        self,
        query: str,
        top_k: int = 5,
        metadata_filter: dict[str, Any] | None = None,
        temperature: float = 0.2,
        max_tokens: int = 500,
    ):
        results, messages, sources = self._prepare(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )

        yield {
            "type": "sources",
            "sources": sources,
            "retrieved_chunks": len(results),
        }

        async for token in self.llm.stream(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            yield {
                "type": "token",
                "content": token,
            }

        yield {
            "type": "done",
        }