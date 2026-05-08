from collections import deque
from app.config import settings


class MemoryStore:
    def __init__(self):
        self.sessions = {}

    def add(
        self,
        session_id,
        role,
        content
    ):
        if session_id not in self.sessions:
            self.sessions[
                session_id
            ] = deque(
                maxlen=
                settings.MEMORY_WINDOW * 2
            )

        self.sessions[
            session_id
        ].append(
            {
                "role": role,
                "content": content
            }
        )

    def get_context(
        self,
        session_id
    ):
        if session_id not in self.sessions:
            return []

        return list(
            self.sessions[session_id]
        )

    def count(
        self,
        session_id
    ):
        if session_id not in self.sessions:
            return 0

        return len(
            self.sessions[session_id]
        )

    def clear(
        self,
        session_id
    ):
        if session_id in self.sessions:
            del self.sessions[
                session_id
            ]


memory_store = MemoryStore()