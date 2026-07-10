import streamlit as st


def initialize():
    """
    Initialize Streamlit session state.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "uploaded" not in st.session_state:
        st.session_state.uploaded = []

    if "chat_count" not in st.session_state:
        st.session_state.chat_count = 0

    if "upload_count" not in st.session_state:
        st.session_state.upload_count = 0


def add_user_message(message: str):
    """
    Store user message.
    """

    st.session_state.messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    st.session_state.chat_count += 1


def add_assistant_message(
    message: str,
    sources=None
):
    """
    Store assistant response.
    """

    if sources is None:
        sources = []

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": message,
            "sources": sources
        }
    )

    st.session_state.chat_count += 1


def add_uploaded_document(filename: str):
    """
    Track uploaded documents.
    """

    if filename not in st.session_state.uploaded:

        st.session_state.uploaded.append(
            filename
        )

        st.session_state.upload_count += 1


def clear_chat():
    """
    Clear chat history.
    """

    st.session_state.messages = []


def clear_documents():
    """
    Remove uploaded document list.
    Backend database is not affected.
    """

    st.session_state.uploaded = []

    st.session_state.upload_count = 0


def total_messages():

    return len(
        st.session_state.messages
    )


def total_documents():

    return len(
        st.session_state.uploaded
    )