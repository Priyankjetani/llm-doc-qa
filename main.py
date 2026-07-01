import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import storage
from dotenv import load_dotenv
import PyPDF2
import io
import os

# Load your settings from .env
load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION   = os.getenv("GCP_LOCATION")
BUCKET     = os.getenv("GCP_BUCKET")
DOC_PATH   = "docs/mydoc.pdf"

# Connect to Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)


def read_pdf_from_gcs(bucket_name, blob_name):
    """Downloads the PDF from GCP and extracts its text"""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    data = blob.download_as_bytes()
    
    reader = PyPDF2.PdfReader(io.BytesIO(data))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def ask_question(doc_text, question):
    """Sends the document + question to Gemini and gets an answer"""
    model = GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""You are a helpful assistant answering questions about a document.
The document text below may have unusual spacing or line breaks from PDF extraction — 
read through that and understand the actual content/meaning.

Answer the question using the document below.
If the answer truly cannot be found, say "Not found in document."

DOCUMENT:
{doc_text}

QUESTION: {question}
ANSWER:"""
    
    response = model.generate_content(prompt)
    return response.text


def main():
    print("📄 Loading document from GCS...")
    doc_text = read_pdf_from_gcs(BUCKET, DOC_PATH)
    print(f"✅ Document loaded ({len(doc_text)} characters)\n")
    
    # 🔍 DEBUG: print first 300 characters to check extraction
    # print("--- DEBUG: First 300 chars of extracted text ---")
    # print(doc_text)
    # print("--- END DEBUG ---\n")
    
    print("💬 Ask me anything about this document (type 'quit' to exit)\n")
    
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            print("👋 Goodbye!")
            break
        
        answer = ask_question(doc_text, question)
        print(f"\nAI: {answer}\n")


if __name__ == "__main__":
    main()
