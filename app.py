from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import storage
from dotenv import load_dotenv
import PyPDF2
import io
import os

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION   = os.getenv("GCP_LOCATION")
BUCKET     = os.getenv("GCP_BUCKET")

vertexai.init(project=PROJECT_ID, location=LOCATION)

app = FastAPI(title="Document Q&A Chatbot API")

# Allow requests from a browser frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory store: {filename: extracted_text}
# (We'll upgrade this in Step C for multiple documents)
documents = {}


def extract_pdf_text(file_bytes):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def ask_gemini(doc_text, question):
    model = GenerativeModel("gemini-2.5-flash")
    prompt = f"""You are a helpful assistant answering questions about a document.
The document text below may have unusual spacing from PDF extraction — read past that.

Answer the question using the document below.
If the answer truly cannot be found, say "Not found in document."

DOCUMENT:
{doc_text}

QUESTION: {question}
ANSWER:"""
    response = model.generate_content(prompt)
    return response.text


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF and store its extracted text in memory"""
    file_bytes = await file.read()
    text = extract_pdf_text(file_bytes)
    documents[file.filename] = text

    # Also save a copy to GCP Cloud Storage (optional but good practice)
    client = storage.Client()
    bucket = client.bucket(BUCKET)
    blob = bucket.blob(f"docs/{file.filename}")
    blob.upload_from_string(file_bytes, content_type="application/pdf")

    return {"filename": file.filename, "characters_extracted": len(text)}


@app.post("/ask")
async def ask_question(filename: str = Form(...), question: str = Form(...)):
    """Ask a question about a previously uploaded document"""
    if filename not in documents:
        return {"error": f"Document '{filename}' not found. Upload it first via /upload"}

    answer = ask_gemini(documents[filename], question)
    return {"filename": filename, "question": question, "answer": answer}


@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    return {"documents": list(documents.keys())}


@app.get("/")
async def root():
    return {"message": "Document Q&A API is running. Visit /docs for interactive testing."}