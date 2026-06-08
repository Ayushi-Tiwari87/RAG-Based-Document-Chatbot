"""
RAG CHATBOT SETUP AND DEPLOYMENT GUIDE

This guide provides step-by-step instructions for setting up and running
the production-ready RAG Chatbot application.
"""

# ============================================================================
# 1. INITIAL SETUP
# ============================================================================

# 1.1 Create Python Virtual Environment
# Command:
#   python -m venv venv
#
# Activate (Windows):
#   venv\Scripts\activate
#
# Activate (Mac/Linux):
#   source venv/bin/activate

# 1.2 Install Dependencies
# Command:
#   pip install -r requirements.txt
#
# Verify Installation:
#   python -c "import langchain, chromadb, groq, streamlit; print('✅ All packages installed')"


# ============================================================================
# 2. ENVIRONMENT SETUP
# ============================================================================

# 2.1 Copy Environment Template
# Command:
#   cp .env.example .env

# 2.2 Get Groq API Key
# Steps:
#   1. Go to https://console.groq.com
#   2. Sign up or log in
#   3. Create an API key
#   4. Copy the key

# 2.3 Configure .env File
# Edit .env and set:
#   GROQ_API_KEY=your_key_here
#   ENV=development  # or production
#   LOG_LEVEL=INFO

# 2.4 Verify Configuration
# Command:
#   python app.py
#
# Expected Output:
#   ✅ GROQ_API_KEY is configured
#   ✅ Vector DB path created
#   ✅ Logs directory created


# ============================================================================
# 3. LOCAL DEVELOPMENT
# ============================================================================

# 3.1 Run FastAPI Backend
# Terminal 1:
#   python -m uvicorn api.fastapi_app:app --reload --host 0.0.0.0 --port 8000
#
# Expected:
#   Uvicorn running on http://127.0.0.1:8000
#
# Test Health:
#   curl http://localhost:8000/health

# 3.2 Run Streamlit UI
# Terminal 2:
#   streamlit run ui/streamlit_app.py
#
# Expected:
#   You can now view your Streamlit app in your browser.
#   Local URL: http://localhost:8501

# 3.3 Access Application
# - Frontend: http://localhost:8501
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs


# ============================================================================
# 4. TESTING
# ============================================================================

# 4.1 Run Unit Tests
# Command:
#   pytest tests/ -v

# 4.2 Test Document Ingestion
# Command:
#   pytest tests/test_ingestion.py -v

# 4.3 Test Conversation Memory
# Command:
#   pytest tests/test_memory.py -v

# 4.4 Run with Coverage
# Command:
#   pytest tests/ --cov=. --cov-report=html
#   # Open htmlcov/index.html in browser


# ============================================================================
# 5. API USAGE
# ============================================================================

# 5.1 Health Check
# curl http://localhost:8000/health

# 5.2 Upload Documents (via curl)
# curl -X POST "http://localhost:8000/upload" \
#   -F "files=@document.pdf" \
#   -F "files=@document.docx"

# 5.3 Ingest Documents
# curl -X POST http://localhost:8000/ingest

# 5.4 Query the Chatbot
# curl -X POST "http://localhost:8000/chat" \
#   -H "Content-Type: application/json" \
#   -d '{"query": "What is in the documents?", "k": 5}'

# 5.5 Get Status
# curl http://localhost:8000/status

# 5.6 Delete Documents
# curl -X DELETE http://localhost:8000/documents


# ============================================================================
# 6. DOCKER DEPLOYMENT
# ============================================================================

# 6.1 Prerequisites
# - Docker installed
# - Docker Compose installed
# - .env file configured with GROQ_API_KEY

# 6.2 Build Images
# Command:
#   docker-compose build

# 6.3 Start Services
# Command:
#   docker-compose up -d

# 6.4 Check Logs
# Command:
#   docker-compose logs -f api
#   docker-compose logs -f ui

# 6.5 Access Services
# - API: http://localhost:8000
# - UI: http://localhost:8501
# - API Docs: http://localhost:8000/docs

# 6.6 Stop Services
# Command:
#   docker-compose down

# 6.7 Remove Volumes (Clean Reset)
# Command:
#   docker-compose down -v


# ============================================================================
# 7. PRODUCTION DEPLOYMENT
# ============================================================================

# 7.1 Environment Variables
# Set these in your production environment:
#   ENV=production
#   LOG_LEVEL=INFO
#   GROQ_API_KEY=<your_key>
#   FASTAPI_HOST=0.0.0.0
#   FASTAPI_PORT=8000

# 7.2 Docker Compose Production
# Command:
#   docker-compose -f docker-compose.yml up -d

# 7.3 Enable HTTPS (nginx reverse proxy)
# Create nginx.conf with SSL configuration
# Map ports: 443 → 8000 (API), 8501 (UI)

# 7.4 Health Monitoring
# Command:
#   curl -f http://localhost:8000/health || echo "API down"

# 7.5 Backup Data
# Command (Unix):
#   tar -czf backup_$(date +%Y%m%d).tar.gz vectordb/ data/ logs/
#
# Command (Windows):
#   Compress-Archive -Path "vectordb", "data", "logs" -DestinationPath "backup_$(Get-Date -f 'yyyyMMdd').zip"

# 7.6 Restore Data
# Command (Unix):
#   tar -xzf backup_YYYYMMDD.tar.gz
#
# Command (Windows):
#   Expand-Archive -Path "backup_YYYYMMDD.zip" -DestinationPath .


# ============================================================================
# 8. TROUBLESHOOTING
# ============================================================================

# 8.1 Port Already in Use
# Find Process (Windows):
#   netstat -ano | findstr :8000
#   taskkill /PID <PID> /F
#
# Find Process (Unix):
#   lsof -i :8000
#   kill -9 <PID>
#
# Use Different Port:
#   FASTAPI_PORT=8001 python -m uvicorn api.fastapi_app:app

# 8.2 Groq API Key Invalid
# Check:
#   - Key is valid and not expired
#   - Key is set correctly in .env
#   - No extra spaces or quotes
# Verify:
#   python -c "from groq import Groq; print(Groq().models.list())"

# 8.3 Embedding Generation Slow
# Solutions:
#   - Use faster model: BAAI/bge-tiny-en-v1.5
#   - Reduce EMBEDDING_BATCH_SIZE
#   - Use GPU (install torch with CUDA)

# 8.4 Out of Memory
# Solutions:
#   - Reduce CHUNK_SIZE
#   - Reduce EMBEDDING_BATCH_SIZE
#   - Process fewer documents at once
#   - Increase system RAM

# 8.5 Streamlit Timeout
# Set in streamlit config:
#   [client]
#   maxMessageSize = 200


# ============================================================================
# 9. PERFORMANCE TUNING
# ============================================================================

# 9.1 Faster Embeddings
# Use smaller model in .env:
#   EMBEDDING_MODEL=BAAI/bge-tiny-en-v1.5
#
# Or with quantization (requires transformers):
#   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# 9.2 Faster Retrieval
# Reduce RETRIEVAL_K:
#   RETRIEVAL_K=3  # instead of 5

# 9.3 Reduce Memory Usage
# Set in .env:
#   EMBEDDING_BATCH_SIZE=8  # instead of 32

# 9.4 Enable GPU (if available)
# Install CUDA-enabled PyTorch:
#   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118


# ============================================================================
# 10. MONITORING AND MAINTENANCE
# ============================================================================

# 10.1 Check Logs
# File Location: logs/app.log
# View Last 50 Lines:
#   tail -50 logs/app.log  # Unix
#   Get-Content logs/app.log -Tail 50  # Windows

# 10.2 Monitor Database Size
# Check Vector DB Size:
#   du -sh vectordb/  # Unix
#   (Get-Item "vectordb" -Recurse | Measure-Object -Sum Length).Sum  # Windows

# 10.3 Clear Old Logs
# Command (Unix):
#   find logs/ -name "*.log" -mtime +30 -delete
#
# Command (Windows):
#   # Use Log Viewer or cleanup script

# 10.4 Database Maintenance
# Clear Old Collections:
#   python -c "from vectordb.vector_database import VectorDatabase; db = VectorDatabase(); db.delete_collection()"

# 10.5 Performance Metrics
# Check in logs for:
#   - Query processing time
#   - Number of documents retrieved
#   - API response times
#   - Embedding generation time


# ============================================================================
# 11. SECURITY
# ============================================================================

# 11.1 Protect API Keys
# Never commit .env file:
#   echo ".env" >> .gitignore

# 11.2 Enable API Authentication (Optional)
# Add to FastAPI app for production:
#   from fastapi.security import HTTPBearer, HTTPAuthCredential

# 11.3 Rate Limiting (Optional)
# Install slowapi:
#   pip install slowapi
# Add to FastAPI app

# 11.4 HTTPS/SSL (Required for production)
# Use nginx or Apache as reverse proxy
# Configure SSL certificates (Let's Encrypt)

# 11.5 Input Validation
# Already implemented in:
#   - api/fastapi_app.py (query length limits)
#   - ingestion/document_ingestion.py (file validation)


# ============================================================================
# 12. ADVANCED CONFIGURATION
# ============================================================================

# 12.1 Custom Prompt Template
# Edit in llm/groq_client.py:
#   SYSTEM_PROMPT = "Your custom prompt here"

# 12.2 Multiple Collections
# Create separate databases:
#   db1 = VectorDatabase("collection_1")
#   db2 = VectorDatabase("collection_2")

# 12.3 Custom Embedding Model
# In .env:
#   EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2

# 12.4 Different LLM Models (Groq)
# Available models:
#   - llama-2-70b-chat
#   - mixtral-8x7b-32768
#   - gemma-7b-it
#   - llama-3.3-70b-versatile (default)


# ============================================================================
# 13. INTEGRATION EXAMPLES
# ============================================================================

# 13.1 Python Integration
"""
from rag_pipeline import RAGPipeline

# Initialize
rag = RAGPipeline()

# Ingest documents
rag.ingest_documents(["document.pdf", "data.docx"])

# Query
result = rag.query("What is the main topic?")
print(result["response"])
print(f"Sources: {result['sources']}")
"""

# 13.2 API Integration
"""
import requests

# Chat
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "query": "Your question here",
        "k": 5
    }
)

result = response.json()
print(result["response"])
"""

# 13.3 Async Integration
"""
import asyncio
from httpx import AsyncClient

async def query_rag():
    async with AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/chat",
            json={"query": "Question?"}
        )
        return response.json()

result = asyncio.run(query_rag())
"""


# ============================================================================
# 14. COMMON RECIPES
# ============================================================================

# 14.1 Batch Process Documents
"""
import os
from rag_pipeline import RAGPipeline

rag = RAGPipeline()
doc_dir = "documents/"
files = [os.path.join(doc_dir, f) for f in os.listdir(doc_dir)]
rag.ingest_documents(files)
"""

# 14.2 Export Chat History
"""
from utils.conversation_memory import ConversationMemory

memory = ConversationMemory()
memory.load_from_file("conversation.json")
memory.save_to_file("conversation_backup.json")
"""

# 14.3 Search and Export Results
"""
from retrieval.retriever_system import RetrieverSystem

retriever = RetrieverSystem()
docs = retriever.retrieve("query text", k=10)

for doc in docs:
    print(f"Source: {doc.metadata['source']}")
    print(f"Content: {doc.page_content[:200]}")
"""


# ============================================================================
# NEED HELP?
# ============================================================================

# Check logs:
#   tail -f logs/app.log

# Verify API is running:
#   curl http://localhost:8000/health

# Check configuration:
#   python app.py

# Run tests:
#   pytest tests/ -v

# View API documentation:
#   http://localhost:8000/docs
#   http://localhost:8000/redoc

# Visit GitHub (if available):
#   https://github.com/yourusername/rag-chatbot

# ============================================================================
