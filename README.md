# AI Fake News Detector

An advanced, AI-powered platform designed to detect and analyze potential fake news using state-of-the-art Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG). This project leverages local LLM execution with Ollama and factual verification via a custom knowledge base.

---

## Overview
In an era of information overload, the **AI Fake News Detector** provides a robust solution for verifying the authenticity of news articles. By combining web scraping, vector-based information retrieval, and intelligent chat capabilities, it helps users distinguish between verified facts and misinformation.

The system uses a **RAG (Retrieval-Augmented Generation)** pipeline to ensure that the AI's responses are grounded in verified data, reducing hallucinations and providing context-aware analysis.

---

## Features
- **Intelligent URL Analysis**: Scrape news articles directly from URLs for instant content extraction and analysis.
- **RAG-Powered Chat**: Interact with an AI assistant that uses a local knowledge base to verify claims.
- **Session-Based History**: Persistent chat history stored in a local SQLite database for continuous context.
- **Automated Maintenance**: Periodic cleanup of expired sessions to ensure optimal performance.
- **Vector Knowledge Base**: Uses ChromaDB to store and retrieve verified facts for factual grounding.
- **Local LLM Execution**: Runs entirely on your local machine using Ollama, ensuring privacy and cost-efficiency.

---

## Tech Stack
- **Backend**: Python 3.10+, FastAPI
- **LLM Orchestration**: LangChain
- **Local LLM**: Ollama (Default: `gemma3:1b`)
- **Vector Database**: ChromaDB
- **Database**: SQLite (SQLAlchemy)
- **Scraping**: Newspaper3k
- **Embeddings**: Sentence-Transformers

---

## Setup Instructions

### 1. Prerequisites
- Python 3.10 or higher
- [Ollama](https://ollama.ai/) installed and running
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/AIFakeNewsDetector.git
cd AIFakeNewsDetector
```

### 3. Environment Configuration
Create a `.env` file in the `rag_app/` directory (or use the template from the root):
```bash
cp .env.example rag_app/.env
```
Edit `rag_app/.env` and provide your configuration:
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:1b
```

### 4. Install Dependencies
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 5. Initialize the Knowledge Base
Ingest sample verified data into the vector store:
```bash
python -m rag_app.src.rag.ingest
```

### 6. Run the Application
```bash
uvicorn rag_app.src.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

---

## Usage

### API Endpoints

#### 1. Analyze a News URL
**POST** `/analyze-url?url={URL}`
Extracts content from a URL and provides an initial fake/real prediction.

#### 2. Chat with RAG Assistance
**POST** `/chat`
**Body:**
```json
{
  "question": "Is there any evidence that 5G spreads COVID-19?",
  "session_id": "optional-session-id",
  "model": "gemma3:1b"
}
```

#### 3. Get Session History
**GET** `/session/{session_id}`
Retrieves all messages for a specific session.

---

## Project Structure
```text
AIFakeNewsDetector/
├── rag_app/                # Main application directory
│   ├── src/
│   │   ├── api/            # FastAPI routes
│   │   ├── core/           # LLM and core configurations
│   │   ├── db/             # Database models and session management
│   │   ├── rag/            # RAG pipeline (embeddings, vector store)
│   │   ├── scraper/        # Web scraping logic
│   │   ├── services/       # Business logic services
│   │   ├── utils/          # Helper functions
│   │   └── main.py         # Application entry point
│   ├── data/               # Raw data storage
│   └── chroma_db/          # Persistent vector database
├── test/                   # Unit and integration tests
├── requirements.txt        # Project dependencies
└── .env.example            # Environment configuration template
```

---

## Future Improvements
- [ ] Integration with real-time fact-checking APIs (e.g., Google Fact Check).
- [ ] Support for multi-modal analysis (images and videos).
- [ ] Enhanced ML models for linguistic feature analysis.
- [ ] User dashboard for tracking analyzed articles.
- [ ] Chrome extension for on-the-fly news verification.

---

## Author
**Gayuth**
- [GitHub](https://github.com/Gayuth-W)
- [LinkedIn](https://linkedin.com/in/gayuth)