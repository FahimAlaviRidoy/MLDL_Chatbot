from pathlib import Path
from pypdf import PdfReader


class Loader:

    @staticmethod
    def load_pdf(file_path):
        reader = PdfReader(file_path)

        docs = []

        for i, page in enumerate(
            reader.pages
        ):
            text = page.extract_text()

            if text and text.strip():
                docs.append(
                    {
                        "text": text.strip(),
                        "source": Path(file_path).name,
                        "page": i + 1
                    }
                )

        return docs

    @staticmethod
    def load_text(
        text,
        title="manual_text"
    ):
        return [
            {
                "text": text.strip(),
                "source": title,
                "page": 1
            }
        ]