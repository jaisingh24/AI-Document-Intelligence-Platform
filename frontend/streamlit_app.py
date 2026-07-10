import streamlit as st

from api import upload_document, ask_question
from utils import initialize

initialize()

st.set_page_config(
    page_title="AI Document Intelligence Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------
# Header
# -------------------------------

st.title("🤖 AI Document Intelligence Platform")

st.markdown(
    """
Semantic Search • Retrieval-Augmented Generation (RAG) • FastAPI • ChromaDB • Jina Embeddings • Groq
"""
)

st.divider()

# -------------------------------
# Sidebar
# -------------------------------

with st.sidebar:

    st.header("📂 Documents")

    uploaded = st.file_uploader(
        "Upload Document",
        type=["pdf", "txt", "md"]
    )

    if uploaded:

        if st.button(
            "📤 Upload",
            use_container_width=True
        ):

            with st.spinner("Indexing document..."):

                try:

                    result = upload_document(uploaded)

                    st.success("Document indexed successfully!")

                    st.info(
                        f"""
Filename : {uploaded.name}

Chunks : {result['chunks']}
"""
                    )

                    if uploaded.name not in st.session_state.uploaded:
                        st.session_state.uploaded.append(uploaded.name)

                except Exception as e:

                    st.error(str(e))

    st.divider()

    st.subheader("📚 Indexed Documents")

    if st.session_state.uploaded:

        for doc in st.session_state.uploaded:

            st.success(f"📄 {doc}")

    else:

        st.caption("No documents uploaded.")

    st.divider()

    st.subheader("📊 Statistics")

    st.metric(
        "Documents",
        len(st.session_state.uploaded)
    )

    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

    st.divider()

    if st.button(
        "🗑 Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

# -------------------------------
# Welcome Screen
# -------------------------------

if len(st.session_state.messages) == 0:

    st.info(
        """
### 👋 Welcome

Upload one or more documents and start asking questions.

Example Questions

• What is Microservices?

• Explain API Gateway

• What books are recommended?

• Summarize this document.

• What should I learn first?
"""
    )

# -------------------------------
# Chat Messages
# -------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander("📄 Sources"):

                for source in message["sources"]:

                    if isinstance(source, dict):

                        st.markdown(
                            f"""
**Document**

{source.get("document")}

**Page**

{source.get("page")}
"""
                        )

                        st.divider()

                    else:

                        st.markdown(f"📄 {source}")

# -------------------------------
# Chat Input
# -------------------------------

question = st.chat_input(
    "Ask a question about your documents..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        placeholder.markdown("⏳ Thinking...")

        try:

            response = ask_question(question)

            answer = response["answer"]

            sources = response.get(
                "sources",
                []
            )

            placeholder.markdown(answer)

            if sources:

                with st.expander("📄 Sources"):

                    for source in sources:

                        if isinstance(source, dict):

                            st.markdown(
                                f"""
**Document**

{source.get("document")}

**Page**

{source.get("page")}
"""
                            )

                            st.divider()

                        else:

                            st.markdown(f"📄 {source}")

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                }
            )

        except Exception as e:

            placeholder.empty()

            st.error(str(e))

# -------------------------------
# Footer
# -------------------------------

st.divider()

st.caption(
    "Powered by FastAPI • ChromaDB • Jina Embeddings • Groq"
)