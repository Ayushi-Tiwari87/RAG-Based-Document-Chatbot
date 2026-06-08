# RAG Chatbot - Production-Ready Retrieval-Augmented Generation System

A complete, production-ready Retrieval-Augmented Generation (RAG) chatbot built with modern AI engineering best practices. Upload documents (PDF, DOCX, TXT), store embeddings, and chat with AI-powered retrieval using Groq LLMs.

## 🎯 Features

- **Document Ingestion**: Support for PDF, DOCX, and TXT files
- **Vector Storage**: ChromaDB for persistent embedding storage
- **Semantic Search**: Retrieve relevant documents using embeddings
- **LLM Integration**: Groq API integration with Llama 3.3 70B model
- **Conversation Memory**: Session-based chat history management
- **FastAPI Backend**: RESTful API for document management and chat
- **Streamlit UI**: Modern, responsive web interface
- **Batch Processing**: Efficient embedding generation and retrieval
- **Source Attribution**: Track and cite document sources
- **Production Ready**: Docker support, logging, security features

## 📋 Prerequisites

- Python 3.12+
- Docker & Docker Compose (optional, for containerized deployment)
- Groq API Key ([Get it here](https://console.groq.com))

## 🚀 Quick Start

### 1. Setup Environment

```bash
cd rag_chatbot
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

**Terminal 1 - Start FastAPI Backend:**
```bash
python -m uvicorn api.fastapi_app:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Streamlit UI:**
```bash
streamlit run ui/streamlit_app.py
```

The application will be available at:
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- UI: `http://localhost:8501`

### 4. Docker Deployment (Optional)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access services:
# API: http://localhost:8000
# UI: http://localhost:8501
```

## 📁 Project Structure

```
rag_chatbot/
│
├── api/                           # FastAPI backend
│   ├── fastapi_app.py            # Main API application
│   └── __init__.py
│
├── ui/                            # Streamlit frontend
│   ├── streamlit_app.py          # Web interface
│   └── __init__.py
│
├── ingestion/                     # Document processing
│   ├── document_ingestion.py     # Loaders & chunking
│   └── __init__.py
│
├── llm/                           # LLM & embedding modules
│   ├── groq_client.py            # Groq API wrapper
│   ├── embedding_generator.py    # HuggingFace embeddings
│   └── __init__.py
│
├── vectordb/                      # Vector database
│   ├── vector_database.py        # ChromaDB wrapper
│   └── __init__.py
│
├── retrieval/                     # Retrieval system
│   ├── retriever_system.py       # Semantic search
│   └── __init__.py
│
├── utils/                         # Utility modules
│   ├── conversation_memory.py    # Chat history
│   └── __init__.py
│
├── tests/                         # Unit & integration tests
│   ├── test_ingestion.py
│   ├── test_memory.py
│   └── __init__.py
│
├── data/                          # Uploaded documents
├── vectordb/                      # Vector DB storage
├── logs/                          # Application logs
│
├── rag_pipeline.py               # Core RAG orchestrator
├── config.py                      # Configuration management
├── logger.py                      # Logging setup
├── app.py                         # Entry point
│
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── Dockerfile                     # API container
├── Dockerfile.streamlit          # UI container
├── docker-compose.yml            # Multi-container setup
├── .gitignore                    # Git ignore rules
└── README.md                     # Documentation
```

## 🔧 Configuration

Edit `.env` file to customize settings:

### Document Processing
```
CHUNK_SIZE=1000              # Size of document chunks
CHUNK_OVERLAP=200            # Overlap between chunks
MAX_FILE_SIZE_MB=100         # Maximum file size
```

### Embedding
```
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5  # HuggingFace model
EMBEDDING_BATCH_SIZE=32                  # Batch size
```

### Retrieval
```
RETRIEVAL_K=5                # Number of documents to retrieve
SIMILARITY_THRESHOLD=0.3     # Minimum similarity score
```

### LLM
```
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2048
LLM_TIMEOUT=30
LLM_MAX_RETRIES=3
```

### Application
```
LOG_LEVEL=INFO               # Logging level
ENV=development              # development or production
```

## 📚 API Endpoints

### Health Check
```bash
GET /health
```

### Chat
```bash
POST /chat
Content-Type: application/json

{
  "query": "What is in the documents?",
  "k": 5,
  "use_history": true,
  "stream": false
}
```

### Upload Documents
```bash
POST /upload
Content-Type: multipart/form-data

[files]
```

### Ingest Documents
```bash
POST /ingest
```

### Get Status
```bash
GET /status
```

### Delete Documents
```bash
DELETE /documents
```

## 🎨 Usage

### 1. Upload Documents
- Use the Streamlit UI sidebar to upload PDF, DOCX, or TXT files
- Click "📤 Upload Files" to upload
- Click "🔄 Ingest Documents" to process and store embeddings

### 2. Ask Questions
- Type your question in the chat input
- The system retrieves relevant documents and generates an answer
- Sources are displayed below each response

### 3. Manage Data
- View system status in the sidebar
- Adjust retrieval parameters (Top K documents)
- Clear chat history or delete all documents

## 🧪 Testing

Run unit tests:
```bash
pytest tests/ -v

# With coverage:
pytest tests/ --cov=. --cov-report=html
```

Run specific test:
```bash
pytest tests/test_ingestion.py -v
```

## 🔐 Security Features

- **Input Validation**: File type and size validation
- **API Protection**: Query length limits
- **Environment Variables**: Sensitive data in `.env`
- **Error Handling**: Graceful error messages without exposing internals
- **Timeout Protection**: Request timeouts to prevent hanging

## 📊 Performance Optimization

- **Batch Embedding**: Process multiple documents efficiently
- **Vector DB Persistence**: ChromaDB persistent storage
- **Lazy Loading**: Load models only when needed
- **Caching**: Embedding reuse across queries
- **Efficient Retrieval**: Fast similarity search with filtering

## 📝 Logging

Application logs are stored in `logs/app.log` with:
- Timestamp
- Log level (DEBUG, INFO, WARNING, ERROR)
- Logger name
- Message
- Auto-rotating logs (10MB max per file, 5 backups)

View logs:
```bash
tail -f logs/app.log
```

## 🐛 Troubleshooting

### API Won't Start
```bash
# Check if port is in use
lsof -i :8000  # Unix/Mac
netstat -ano | findstr :8000  # Windows

# Use different port
FASTAPI_PORT=8001 python -m uvicorn api.fastapi_app:app
```

### Streamlit Connection Issues
```bash
# Update API endpoint in UI
# Sidebar → API Endpoint → http://localhost:8000
```

### Out of Memory
- Reduce `EMBEDDING_BATCH_SIZE`
- Process fewer documents at once
- Increase system RAM or use GPU

### Slow Embeddings
- Use faster model: `BAAI/bge-tiny-en-v1.5`
- Enable GPU acceleration (requires CUDA)
- Reduce batch size

## 🚢 Production Deployment

### Docker Compose (Recommended)
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f api
docker-compose logs -f ui

# Stop services
docker-compose down
```

### Environment Variables for Production
```bash
ENV=production
LOG_LEVEL=INFO
GROQ_API_KEY=<your_key>
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

### Health Monitoring
```bash
# Check API health
curl http://localhost:8000/health

# Get system status
curl http://localhost:8000/status
```

### Backup & Recovery
```bash
# Backup vector database
cp -r vectordb/ vectordb_backup/

# Restore from backup
rm -r vectordb/
cp -r vectordb_backup/ vectordb/
```

## 📚 Dependencies

- **LangChain**: Framework for building LLM applications
- **ChromaDB**: Vector database for embeddings
- **Groq API**: High-speed LLM inference
- **Sentence Transformers**: State-of-the-art embeddings
- **FastAPI**: Modern Python web framework
- **Streamlit**: Rapid web app framework
- **PyPDF**: PDF processing
- **python-docx**: DOCX processing

See `requirements.txt` for full dependency list.

## 🔄 Workflow Diagram

```
User Query
    ↓
[Query Expansion] → Enhance with conversation history
    ↓
[Vector Search] → Retrieve similar documents
    ↓
[Context Assembly] → Format documents as context
    ↓
[LLM Generation] → Generate response with Groq API
    ↓
[Source Attribution] → Add citation information
    ↓
Response to User
```

## 🎓 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [Groq API Docs](https://console.groq.com/docs)
- [Streamlit Tutorial](https://docs.streamlit.io/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)

## 💡 Best Practices

1. **Document Quality**: Use clean, well-formatted documents for better results
2. **Chunk Size**: Adjust based on your domain (smaller for QA, larger for summarization)
3. **Retrieval K**: Start with 5, increase if missing relevant documents
4. **Temperature**: 0.7 for balanced responses, lower for accuracy, higher for creativity
5. **Regular Backups**: Backup `vectordb/` directory regularly
6. **Monitor Logs**: Check `logs/app.log` for issues and performance metrics

## 📈 Scaling Tips

- **Horizontal**: Deploy multiple API instances behind a load balancer
- **Vertical**: Increase resources (CPU, RAM, GPU)
- **Database**: Migrate to cloud vector DB (Pinecone, Weaviate) for scale
- **LLM**: Use Groq's load balancing for high-throughput scenarios
- **Caching**: Implement Redis for frequent queries

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional document formats (HTML, markdown)
- Advanced query expansion techniques
- Multi-language support
- User authentication
- Web search integration
- Real-time collaborative chat

## 📄 License

This project is provided as-is for educational and commercial use.

## 🙋 Support

For issues and questions:
1. Check troubleshooting section
2. Review logs in `logs/app.log`
3. Test with simple documents first
4. Verify Groq API key is valid

## 🎉 Quick Wins

- Get started in 5 minutes with Docker
- No database setup required (SQLite-like ChromaDB)
- Works on CPU (GPU optional for faster embeddings)
- Minimal configuration needed
- Production-ready out of the box

---

**Built with ❤️ using Python, LangChain, ChromaDB, and Groq APIs**

For detailed setup and troubleshooting, see the full documentation above.
