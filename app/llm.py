from huggingface_hub import (
    InferenceClient
)
from app.config import settings


class LocalLLM:
    def __init__(self):
        print(
            "Connecting to Hugging Face..."
        )

        self.client = InferenceClient(
            model=settings.HF_MODEL,
            token=settings.HF_TOKEN
        )

        print(
            "Connected."
        )

    def generate(
        self,
        prompt
    ):
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        output = (
            self.client
            .chat_completion(
                messages=messages,
                max_tokens=512,
                temperature=0.2
            )
        )

        return (
            output
            .choices[0]
            .message.content
            .strip()
        )


llm = LocalLLM()