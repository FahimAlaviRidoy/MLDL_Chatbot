from gpt4all import GPT4All
from app.config import settings


class LocalLLM:
    def __init__(self):
        print(
            "Loading GPT4All model..."
        )

        self.model = GPT4All(
            settings.MODEL_NAME
        )

        print(
            "GPT4All loaded."
        )

    def generate(
        self,
        prompt
    ):
        with self.model.chat_session():
            response = self.model.generate(
                prompt,
                max_tokens=512,
                temp=0.2
            )

        return response.strip()


llm = LocalLLM()