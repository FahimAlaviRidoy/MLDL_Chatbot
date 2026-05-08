from app.config import settings


class Fallback:

    @staticmethod
    def should_fallback(
        results
    ):
        if not results:
            return True

        best_score = results[0][
            "score"
        ]

        return (
            best_score <
            settings
            .SIMILARITY_THRESHOLD
        )

    @staticmethod
    def response():
        return (
            "I couldn't find "
            "that information "
            "in the knowledge base."
        )


fallback = Fallback()