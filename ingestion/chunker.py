import uuid


class Chunker:
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 150

    @classmethod
    def split_text(cls, text):
        chunks = []

        start = 0
        length = len(text)

        while start < length:
            end = start + cls.CHUNK_SIZE

            chunk = text[start:end]

            chunks.append(chunk)

            start += (
                cls.CHUNK_SIZE
                - cls.CHUNK_OVERLAP
            )

        return chunks

    @classmethod
    def chunk_documents(cls, docs):
        all_chunks = []

        for doc in docs:
            pieces = cls.split_text(
                doc["text"]
            )

            for i, piece in enumerate(
                pieces
            ):
                all_chunks.append(
                    {
                        "id": str(
                            uuid.uuid4()
                        ),
                        "text": piece,
                        "metadata": {
                            "source": doc[
                                "source"
                            ],
                            "page": doc[
                                "page"
                            ],
                            "chunk_index": i
                        }
                    }
                )

        return all_chunks