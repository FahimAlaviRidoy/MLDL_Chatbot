from sentence_transformers import (
    SentenceTransformer
)
from app.config import settings
import numpy as np


class Embedder:
    def __init__(self):
        print(
            "Loading embedding model..."
        )

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

        print(
            "Embedding model loaded."
        )

    def embed(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return np.array(
            vectors
        ).tolist()


embedder = Embedder()