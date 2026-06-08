#!/bin/bash
# RAG CHATBOT - QUICK START SCRIPT

echo "=================================================="
echo "RAG Chatbot - Quick Start Setup"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Copy environment template${NC}"
cp .env.example .env
echo "✓ Created .env file"
echo ""

echo -e "${YELLOW}Step 2: Add your GROQ_API_KEY${NC}"
echo "Get your free key from: https://console.groq.com"
echo "Edit .env and add your GROQ_API_KEY"
echo ""
read -p "Press Enter after adding GROQ_API_KEY to .env..."
echo ""

echo -e "${YELLOW}Step 3: Create virtual environment${NC}"
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
echo "✓ Virtual environment created and activated"
echo ""

echo -e "${YELLOW}Step 4: Install dependencies${NC}"
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

echo -e "${YELLOW}Step 5: Verify installation${NC}"
python -c "import langchain, chromadb, groq; print('✓ All packages verified')"
echo ""

echo -e "${GREEN}=================================================="
echo "✨ Setup Complete!"
echo "==================================================${NC}"
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (API Backend):"
echo "  python -m uvicorn api.fastapi_app:app --reload"
echo ""
echo "Terminal 2 (Streamlit UI):"
echo "  streamlit run ui/streamlit_app.py"
echo ""
echo "Then visit:"
echo "  UI: http://localhost:8501"
echo "  API: http://localhost:8000"
echo "  Docs: http://localhost:8000/docs"
echo ""
echo "Or use Docker:"
echo "  docker-compose up --build"
echo ""
