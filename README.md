# Document Q&A Chatbot (RAG with Gemini + GCP)

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about uploaded PDF documents using Google Cloud's Vertex AI (Gemini 2.5 Flash) and Cloud Storage.

## Features
- Upload any PDF document via a REST API
- Ask natural language questions about the document's content
- Supports multiple documents simultaneously
- Documents are stored in Google Cloud Storage
- Built with FastAPI — includes auto-generated interactive API docs

## Tech Stack
- **Python 3**
- **FastAPI** — REST API framework
- **Google Cloud Vertex AI** — Gemini 2.5 Flash for LLM responses
- **Google Cloud Storage** — document storage
- **PyPDF2** — PDF text extraction

## Architecture

PDF Upload → Text Extraction (PyPDF2) → Cloud Storage (backup)
→ In-memory store
→ Gemini 2.5 Flash (RAG prompt)
→ Answer returned via API

## Setup

1. Clone this repo
```bash
git clone https://github.com/YOUR-USERNAME/llm-doc-qa.git
cd llm-doc-qa
```

2. Create virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up your `.env` file

GOOGLE_APPLICATION_CREDENTIALS=path/to/your/key.json
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
GCP_BUCKET=your-bucket-name

4. Run the API
```bash
uvicorn app:app --reload
```

5. Open `http://127.0.0.1:8000/docs` to test interactively

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload a PDF document |
| POST | `/ask` | Ask a question about an uploaded document |
| GET | `/documents` | List all uploaded documents |
| GET | `/` | Health check |

## Example Usage

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -F "filename=resume.pdf" \
  -F "question=What skills does this candidate have?"
```

## Future Improvements
- Add vector embeddings for better retrieval on longer documents
- Add persistent database instead of in-memory storage
- Add a simple frontend UI

## Author
Priyank Jetani — [LinkedIn](https://www.linkedin.com/in/priyank-jetani) | [GitHub](https://github.com/Priyankjetani)