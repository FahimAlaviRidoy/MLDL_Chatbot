import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "mistral-7b-instruct-v0.1.Q4_0.gguf"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "BAAI/bge-small-en-v1.5"
    )

    CHROMA_PATH = os.getenv(
        "CHROMA_PATH",
        "./chroma_db"
    )

    TOP_K = int(
        os.getenv("TOP_K", 5)
    )

    SIMILARITY_THRESHOLD = float(
        os.getenv(
            "SIMILARITY_THRESHOLD",
            0.55
        )
    )

    MEMORY_WINDOW = int(
        os.getenv("MEMORY_WINDOW", 5)
    )

    MAX_CONTEXT_CHUNKS = int(
        os.getenv(
            "MAX_CONTEXT_CHUNKS",
            4
        )
    )


settings = Settings()