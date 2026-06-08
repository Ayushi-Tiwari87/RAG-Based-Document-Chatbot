"""Streamlit UI for RAG Chatbot."""

import os
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for dark mode and styling
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stChatMessage {
        background-color: #262730;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .source-box {
        background-color: #31333d;
        border-left: 4px solid #0084b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #31333d;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_endpoint" not in st.session_state:
    st.session_state.api_endpoint = "http://localhost:8000"
if "query_count" not in st.session_state:
    st.session_state.query_count = 0


def get_api_endpoint():
    """Get API endpoint from config."""
    return os.getenv("API_ENDPOINT", "http://localhost:8000")


@st.cache_resource
def init_api_client():
    """Initialize API client."""
    return get_api_endpoint()


def check_api_health():
    """Check if API is running."""
    try:
        response = requests.get(
            f"{st.session_state.api_endpoint}/health", timeout=2
        )
        return response.status_code == 200
    except:
        return False


def upload_documents(files):
    """Upload documents to the API."""
    if not files:
        return {"uploaded_files": [], "errors": ["No files selected"]}

    with st.spinner("Uploading documents..."):
        try:
            response = requests.post(
                f"{st.session_state.api_endpoint}/upload",
                files=[(f.name, f.getvalue()) for f in files],
                timeout=30,
            )
            return response.json()
        except Exception as e:
            return {"uploaded_files": [], "errors": [str(e)]}


def ingest_documents():
    """Ingest uploaded documents."""
    with st.spinner("Ingesting documents into vector database..."):
        try:
            response = requests.post(
                f"{st.session_state.api_endpoint}/ingest",
                timeout=60,
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}


def query_chatbot(query, k=5):
    """Query the chatbot."""
    try:
        response = requests.post(
            f"{st.session_state.api_endpoint}/chat",
            json={
                "query": query,
                "k": k,
                "use_history": True,
                "stream": False,
            },
            timeout=30,
        )
        return response.json()
    except Exception as e:
        return {
            "query": query,
            "response": f"Error: {str(e)}",
            "sources": [],
            "error": str(e),
        }


def get_system_status():
    """Get system status."""
    try:
        response = requests.get(
            f"{st.session_state.api_endpoint}/status",
            timeout=5,
        )
        return response.json()
    except:
        return {"status": "offline", "documents_in_db": 0}


# Main header
st.markdown("# 🤖 RAG Chatbot")
st.markdown("Upload documents and chat with AI-powered retrieval")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    # API endpoint config
    st.session_state.api_endpoint = st.text_input(
        "API Endpoint:",
        value=st.session_state.api_endpoint,
        help="FastAPI backend endpoint",
    )

    # Check API health
    if check_api_health():
        st.success("✅ API Connected")
    else:
        st.error("❌ API Offline")

    # System status
    st.markdown("### 📊 System Status")
    status = get_system_status()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents", status.get("documents_in_db", 0))
    with col2:
        st.metric("Messages", st.session_state.query_count)

    # Document upload section
    st.markdown("### 📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose documents (PDF, DOCX, TXT):",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Upload documents to build your knowledge base",
    )

    if uploaded_files:
        if st.button("📤 Upload Files", use_container_width=True):
            upload_result = upload_documents(uploaded_files)
            if upload_result.get("uploaded_files"):
                st.success(
                    f"✅ Uploaded {len(upload_result['uploaded_files'])} "
                    "files"
                )
            if upload_result.get("errors"):
                for error in upload_result["errors"]:
                    st.error(error)

        if st.button("🔄 Ingest Documents", use_container_width=True):
            ingest_result = ingest_documents()
            if ingest_result.get("status") == "success":
                st.success(
                    f"✅ Ingested {ingest_result.get('ingested_files', 0)} "
                    "documents"
                )
            else:
                st.error(ingest_result.get("message", "Ingestion failed"))

    # Settings
    st.markdown("### ⚙️ Chat Settings")
    retrieval_k = st.slider(
        "Top K Documents:",
        min_value=1,
        max_value=10,
        value=5,
        help="Number of documents to retrieve",
    )

    # Clear chat and database options
    st.markdown("### 🗑️ Manage Data")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.success("Chat history cleared")

    if st.button("Delete All Documents", use_container_width=True):
        with st.spinner("Deleting documents..."):
            try:
                response = requests.delete(
                    f"{st.session_state.api_endpoint}/documents",
                    timeout=30,
                )
                if response.status_code == 200:
                    st.success("✅ All documents deleted")
                else:
                    st.error("Failed to delete documents")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Main chat interface
st.markdown("## 💬 Chat")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.markdown(
                f"**Sources:** {', '.join(message['sources'])}",
                help="Documents used to answer this question",
            )

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.query_count += 1

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = query_chatbot(prompt, k=retrieval_k)

        # Display response
        response_text = result.get(
            "response", "Error getting response"
        )
        st.markdown(response_text)

        # Display sources
        sources = result.get("sources", [])
        if sources:
            st.markdown(f"**📚 Sources:** {', '.join(sources)}")

        # Display metrics
        col1, col2 = st.columns(2)
        with col1:
            st.caption(
                f"📄 Retrieved {result.get('retrieved_documents', 0)} "
                "documents"
            )
        with col2:
            st.caption(f"⏱️ {datetime.now().strftime('%H:%M:%S')}")

        # Add assistant message to history
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response_text,
                "sources": sources,
            }
        )

# Footer
st.markdown("---")
st.markdown(
    "**RAG Chatbot** powered by LangChain, ChromaDB, and Groq LLMs"
)
