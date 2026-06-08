# RAG CHATBOT - QUICK REFERENCE CARD

## 🚀 GETTING STARTED (5 MINUTES)

### 1. Setup Environment
```bash
# Clone/navigate to project
cd rag_chatbot

# Copy environment template
cp .env.example .env

# Edit .env - add your GROQ_API_KEY
# Get key from: https://console.groq.com
```

### 2. Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix
pip install -r requirements.txt
```

### 3. Run Application
```bash
# Terminal 1: Start API
python -m uvicorn api.fastapi_app:app --reload

# Terminal 2: Start UI
streamlit run ui/streamlit_app.py
```

### 4. Access
- UI: http://localhost:8501
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## 🐳 DOCKER DEPLOYMENT (2 COMMANDS)

```bash
docker-compose build
docker-compose up -d
```

Access:
- UI: http://localhost:8501
- API: http://localhost:8000

---

## 📚 COMMON TASKS

### Upload Documents
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "files=@document.pdf" \
  -F "files=@document.docx"
```

### Ingest Documents
```bash
curl -X POST http://localhost:8000/ingest
```

### Query the Chatbot
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is in the documents?"}'
```

### Clear Database
```bash
curl -X DELETE http://localhost:8000/documents
```

### Check Status
```bash
curl http://localhost:8000/status
curl http://localhost:8000/health
```

---

## ⚙️ CONFIGURATION

Edit `.env`:
```
GROQ_API_KEY=your_key_here
CHUNK_SIZE=1000
RETRIEVAL_K=5
LOG_LEVEL=INFO
```

---

## 🧪 TESTING

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=.

# Test ingestion
pytest tests/test_ingestion.py -v

# Test memory
pytest tests/test_memory.py -v
```

---

## 📊 VIEW LOGS

```bash
tail -f logs/app.log  # Unix/Mac
Get-Content logs/app.log -Tail 50  # Windows PowerShell
```

---

## 🔧 TROUBLESHOOTING

### Port in use?
```bash
# Windows
netstat -ano | findstr :8000

# Unix
lsof -i :8000
```

### API won't connect?
- Check GROQ_API_KEY in .env
- Verify API is running: `curl http://localhost:8000/health`
- Update Streamlit API endpoint in sidebar

### Out of memory?
- Reduce EMBEDDING_BATCH_SIZE in .env
- Reduce CHUNK_SIZE
- Process fewer documents at once

### Slow embeddings?
- Use faster model: `EMBEDDING_MODEL=BAAI/bge-tiny-en-v1.5`
- Reduce RETRIEVAL_K
- Enable GPU (install CUDA-enabled PyTorch)

---

## 📁 PROJECT STRUCTURE

```
rag_chatbot/
├── api/              FastAPI backend
├── ui/               Streamlit frontend
├── ingestion/        Document processing
├── llm/              LLM & embeddings
├── vectordb/         Vector database
├── retrieval/        Semantic search
├── utils/            Utilities
├── tests/            Unit tests
├── data/             Uploaded documents
├── vectordb/         Persistent storage
├── logs/             Application logs
├── requirements.txt  Dependencies
├── .env.example      Configuration template
├── docker-compose.yml Multi-container setup
└── README.md         Full documentation
```

---

## 🔗 API ENDPOINTS

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check API health |
| `/chat` | POST | Query the chatbot |
| `/upload` | POST | Upload documents |
| `/ingest` | POST | Process documents |
| `/status` | GET | Get system status |
| `/documents` | DELETE | Clear database |
| `/docs` | GET | API documentation |

---

## 📚 SUPPORTED FILE TYPES

- `.pdf` - PDF documents
- `.docx` - Microsoft Word
- `.txt` - Plain text

---

## 🎯 KEY FEATURES

✅ Document ingestion (PDF, DOCX, TXT)
✅ Semantic search with embeddings
✅ Groq LLM integration
✅ Conversation memory
✅ Source attribution
✅ FastAPI backend
✅ Streamlit UI
✅ Docker ready
✅ Production grade
✅ Comprehensive logging

---

## 📖 DOCUMENTATION

- **README.md** - Full documentation
- **SETUP_GUIDE.md** - Detailed setup
- **PROJECT_SUMMARY.md** - Project overview
- **API Docs** - http://localhost:8000/docs (interactive)

---

## 🚨 IMPORTANT

⚠️ Never commit `.env` file
⚠️ Keep GROQ_API_KEY secret
⚠️ Use production settings in docker-compose for production
⚠️ Backup vectordb/ directory regularly

---

## ✨ TIPS

💡 Start with small documents to test
💡 Adjust RETRIEVAL_K based on results quality
💡 Use different CHUNK_SIZE for different domains
💡 Monitor logs/app.log for performance metrics
💡 Check /status endpoint for system info

---

## 📞 HELP

- Check README.md for detailed documentation
- View SETUP_GUIDE.md for common issues
- Check logs/app.log for error details
- Run tests to verify setup: `pytest tests/ -v`
- Visit API docs: http://localhost:8000/docs

---

**Last Updated:** 2025-06-07
**Version:** 1.0.0
**Status:** ✅ Production Ready
