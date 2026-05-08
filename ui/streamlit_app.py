import requests
import streamlit as st

import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="KB Chatbot",
    layout="wide"
)

st.title(
    "📚 Private Knowledge Base Chatbot"
)


# session
if "session_id" not in st.session_state:
    r = requests.get(
        f"{API_URL}/session"
    )

    st.session_state.session_id = (
        r.json()["session_id"]
    )

if "messages" not in st.session_state:
    st.session_state.messages = []


sid = st.session_state.session_id


# sidebar
with st.sidebar:
    st.header("Upload Knowledge")

    pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if pdf:
        files = {
            "file": (
                pdf.name,
                pdf,
                "application/pdf"
            )
        }

        r = requests.post(
            f"{API_URL}/upload/pdf",
            params={
                "session_id": sid
            },
            files=files
        )

        st.success(r.json())

    st.divider()

    text = st.text_area(
        "Paste Text"
    )

    title = st.text_input(
        "Title",
        "manual_text"
    )

    if st.button("Add Text"):
        payload = {
            "session_id": sid,
            "text": text,
            "title": title
        }

        r = requests.post(
            f"{API_URL}/upload/text",
            json=payload
        )

        st.success(r.json())

    st.divider()

    st.header("Knowledge Base Stats")

    try:
        stats = requests.get(
            f"{API_URL}/stats/{sid}"
        ).json()

        st.metric(
            "Documents",
            stats[
                "documents_uploaded"
            ]
        )

        st.metric(
            "Chunks",
            stats[
                "chunks_indexed"
            ]
        )

        st.metric(
            "Conversation",
            stats[
                "conversation_messages"
            ]
        )

        st.caption(
            f"Embedding: "
            f"{stats['embedding_model']}"
        )

        st.caption(
            f"LLM: "
            f"{stats['llm_model']}"
        )

        st.caption(
            f"Session: "
            f"{stats['session_id']}"
        )

    except:
        st.info(
            "Stats unavailable"
        )

    st.divider()

    if st.button("Reset Session"):
        requests.post(
            f"{API_URL}/reset",
            json={
                "session_id": sid
            }
        )

        st.session_state.messages = []

        st.success(
            "Reset complete"
        )


# history
for msg in st.session_state.messages:
    with st.chat_message(
        msg["role"]
    ):
        st.write(
            msg["content"]
        )


# input
question = st.chat_input(
    "Ask question..."
)

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    payload = {
        "session_id": sid,
        "question": question
    }

    r = requests.post(
        f"{API_URL}/chat",
        json=payload
    )

    result = r.json()

    answer = result["answer"]

    extra = (
        f"\n\nConfidence: "
        f"{result['confidence']}"
    )

    if result["sources"]:
        extra += "\n\nSources:\n"

        for s in result["sources"]:
            extra += (
                f"- {s['source']} "
                f"(score={s['score']})\n"
            )

    final_answer = answer + extra

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_answer
        }
    )

    with st.chat_message(
        "assistant"
    ):
        st.write(final_answer)