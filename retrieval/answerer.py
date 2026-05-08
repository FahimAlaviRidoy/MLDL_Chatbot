from app.prompts import (
    SYSTEM_PROMPT
)
from app.memory import (
    memory_store
)
from app.llm import llm
from retrieval.retriever import (
    retriever
)
from retrieval.fallback import (
    fallback
)
from app.config import settings


class Answerer:

    @staticmethod
    def build_context(
        results
    ):
        blocks = []

        for r in results[
            :settings
            .MAX_CONTEXT_CHUNKS
        ]:
            source = r[
                "metadata"
            ]["source"]

            page = r[
                "metadata"
            ]["page"]

            block = f"""
SOURCE: {source} (page {page})

CONTENT:
{r["text"]}
"""
            blocks.append(block)

        return "\n\n".join(
            blocks
        )

    @staticmethod
    def build_history(
        session_id
    ):
        history = (
            memory_store
            .get_context(
                session_id
            )
        )

        lines = []

        for item in history:
            role = item[
                "role"
            ].upper()

            content = item[
                "content"
            ]

            lines.append(
                f"{role}: {content}"
            )

        return "\n".join(lines)

    @staticmethod
    def ask(
        session_id,
        question
    ):
        retrieved = (
            retriever.retrieve(
                session_id,
                question
            )
        )

        if fallback.should_fallback(
            retrieved
        ):
            return {
                "answer":
                fallback.response(),
                "confidence":
                0.0,
                "sources": [],
                "fallback": True
            }

        context = (
            Answerer
            .build_context(
                retrieved
            )
        )

        history = (
            Answerer
            .build_history(
                session_id
            )
        )

        prompt = f"""
{SYSTEM_PROMPT}

CHAT HISTORY:
{history}

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

        answer = llm.generate(
            prompt
        )

        memory_store.add(
            session_id,
            "user",
            question
        )

        memory_store.add(
            session_id,
            "assistant",
            answer
        )

        confidence = max(
            [
                r["score"]
                for r in retrieved
            ]
        )

        sources = []

        for r in retrieved[:3]:
            sources.append(
                {
                    "source":
                    r["metadata"][
                        "source"
                    ],
                    "chunk_id":
                    str(
                        r["metadata"][
                            "chunk_index"
                        ]
                    ),
                    "score":
                    r["score"]
                }
            )

        return {
            "answer": answer,
            "confidence":
            round(
                confidence,
                2
            ),
            "sources":
            sources,
            "fallback": False
        }


answerer = Answerer()