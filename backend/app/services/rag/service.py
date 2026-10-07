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
- If the answer cannot be found in the context, clearly say that the information was not found in the provided knowledge base.
- Be concise and directly answer the question.
- When useful, mention the source name from the context.

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

    async def generate(
        self,
        query: str,
        top_k: int = 5,
        metadata_filter: dict[str, Any] | None = None,
        temperature: float = 0.2,
        max_tokens: int = 500,
    ) -> dict[str, Any]:

        results = self.retrieval.retrieve(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )

        context = self.retrieval.build_context(results)

        messages = self._build_prompt(
            query=query,
            context=context,
        )

        answer = await self.llm.generate(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        sources = []

        for result in results:
            metadata = result.get("metadata", {})

            sources.append(
                {
                    "filename": metadata.get("filename"),
                    "score": result.get("score"),
                    "chunk_index": metadata.get("chunk_index"),
                }
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
        results = self.retrieval.retrieve(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )

        context = self.retrieval.build_context(results)

        messages = self._build_prompt(
            query=query,
            context=context,
        )

        async for token in self.llm.stream(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            yield token