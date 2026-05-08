import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    HF_MODEL = os.getenv(
        "HF_MODEL",
        "microsoft/Phi-3-mini-4k-instruct"
    )

    HF_TOKEN = os.getenv(
        "HF_TOKEN"
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
        os.getenv(
            "MEMORY_WINDOW",
            5
        )
    )

    MAX_CONTEXT_CHUNKS = int(
        os.getenv(
            "MAX_CONTEXT_CHUNKS",
            4
        )
    )


settings = Settings()