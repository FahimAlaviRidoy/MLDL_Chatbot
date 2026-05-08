from utils.helpers import generate_hash
from ingestion.loader import Loader
from ingestion.chunker import Chunker
from ingestion.embedder import embedder
from db.chroma_manager import (
    chroma_manager
)


class Ingestor:

    @staticmethod
    def ingest_pdf(
        session_id,
        file_path
    ):
        with open(
            file_path,
            "rb"
        ) as f:
            content = f.read()

        doc_hash = generate_hash(
            content
        )

        if chroma_manager.document_exists(
            session_id,
            doc_hash
        ):
            return {
                "success": False,
                "message":
                "Document already uploaded."
            }

        docs = Loader.load_pdf(
            file_path
        )

        return Ingestor._store(
            session_id,
            docs,
            doc_hash
        )

    @staticmethod
    def ingest_text(
        session_id,
        text,
        title="manual_text"
    ):
        doc_hash = generate_hash(
            text.encode()
        )

        if chroma_manager.document_exists(
            session_id,
            doc_hash
        ):
            return {
                "success": False,
                "message":
                "Text already uploaded."
            }

        docs = Loader.load_text(
            text,
            title
        )

        return Ingestor._store(
            session_id,
            docs,
            doc_hash
        )

    @staticmethod
    def _store(
        session_id,
        docs,
        doc_hash
    ):
        if not docs:
            return {
                "success": False,
                "message":
                "No readable content."
            }

        chunks = Chunker.chunk_documents(
            docs
        )

        texts = [
            c["text"]
            for c in chunks
        ]

        ids = [
            c["id"]
            for c in chunks
        ]

        metadatas = []

        for c in chunks:
            meta = c["metadata"]
            meta["doc_hash"] = doc_hash
            metadatas.append(meta)

        embeddings = embedder.embed(
            texts
        )

        collection = (
            chroma_manager
            .get_or_create_collection(
                session_id
            )
        )

        collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings
        )

        return {
            "success": True,
            "chunks_added":
            len(chunks)
        }


ingestor = Ingestor()