from ingestion.embedder import embedder
from db.chroma_manager import (
    chroma_manager
)
from app.config import settings


class Retriever:

    @staticmethod
    def retrieve(
        session_id,
        question
    ):
        collection = (
            chroma_manager
            .get_or_create_collection(
                session_id
            )
        )

        if collection.count() == 0:
            return []

        q_vector = embedder.embed(
            question
        )[0]

        count = collection.count()

        n_results = min(
            settings.TOP_K,
            count
        )

        results = collection.query(
            query_embeddings=[q_vector],
            n_results=n_results
        )

        docs = results[
            "documents"
        ][0]

        metas = results[
            "metadatas"
        ][0]

        distances = results[
            "distances"
        ][0]

        retrieved = []

        for doc, meta, dist in zip(
            docs,
            metas,
            distances
        ):
            score = max(
                0,
                1 - dist
            )

            retrieved.append(
                {
                    "text": doc,
                    "metadata": meta,
                    "score": round(
                        score,
                        4
                    )
                }
            )

        return retrieved


retriever = Retriever()