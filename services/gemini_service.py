import vertexai
from vertexai.generative_models import GenerativeModel
from core.config import GCP_PROJECT_ID, GCP_LOCATION

vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)


def ask_gemini(doc_text: str, question: str) -> str:
    """Sends document + question to Gemini and returns the answer"""
    model = GenerativeModel("gemini-2.5-flash")
    prompt = f"""You are a helpful assistant answering questions about a document.
The document text may have unusual spacing from PDF extraction — read past that.
Answer using the document below. If the answer is not found, say "Not found in document."

DOCUMENT:
{doc_text}

QUESTION: {question}
ANSWER:"""
    response = model.generate_content(prompt)
    return response.text