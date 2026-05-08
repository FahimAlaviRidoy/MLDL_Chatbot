import chromadb
from chromadb.config import (
    Settings as ChromaSettings
)
from app.config import settings


class ChromaManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PATH,
            settings=ChromaSettings(
                anonymized_telemetry=False
            )
        )

    def collection_name(self, session_id):
        return f"kb_{session_id}"

    def get_or_create_collection(self, session_id):
        name = self.collection_name(session_id)

        return self.client.get_or_create_collection(
            name=name,
            metadata={
                "hnsw:space": "cosine"
            }
        )

    def delete_collection(self, session_id):
        name = self.collection_name(session_id)

        try:
            self.client.delete_collection(name)
            return True
        except Exception:
            return False

    def document_exists(self, session_id, doc_hash):
        collection = self.get_or_create_collection(
            session_id
        )

        results = collection.get(
            where={
                "doc_hash": doc_hash
            }
        )

        return len(results["ids"]) > 0

    def get_stats(self, session_id):
        collection = self.get_or_create_collection(
            session_id
        )

        total_chunks = collection.count()

        docs = collection.get()

        unique_sources = set()

        if docs["metadatas"]:
            for meta in docs["metadatas"]:
                unique_sources.add(
                    meta["source"]
                )

        return {
            "documents": len(unique_sources),
            "chunks": total_chunks
        }


chroma_manager = ChromaManager()