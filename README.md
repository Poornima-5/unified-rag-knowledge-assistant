# Unified RAG Knowledge Assistant

A modular Retrieval-Augmented Generation (RAG) system built with:

- FastAPI (Backend)
- Streamlit (Frontend)
- FAISS (Vector Database)
- HuggingFace Embeddings
- Groq LLM
- MMR Retrieval Strategy

## Supported File Types
- PDF
- DOCX
- TXT
- CSV
- JSON

## Architecture

Frontend (Streamlit)  
      ⬇  
Backend (FastAPI)  
      ⬇  
FAISS per workspace  
      ⬇  
MMR Retriever  
      ⬇  
Groq LLM  

## Setup Instructions

### 1. Create Virtual Environment (using uv)

uv venv  
source .venv/bin/activate (Mac/Linux)  
.venv\Scripts\activate (Windows)

### 2. Install Dependencies

uv add fastapi uvicorn streamlit python-multipart  
uv add langchain langchain-community langchain-core  
uv add langchain-text-splitters langchain-groq  
uv add faiss-cpu sentence-transformers torch  
uv add pandas pypdf docx2txt python-dotenv requests  

### 3. Add .env File

GROQ_API_KEY=your_key_here

### 4. Run Backend

uv run uvicorn backend.main:app --reload

### 5. Run Frontend

uv run streamlit run frontend/app.py
