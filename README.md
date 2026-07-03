An AI-powered document Q&A system built with Python, FastAPI, Google Cloud (Vertex AI + Cloud Storage), Docker, and Kubernetes.

Upload any PDF document, ask questions about it in natural language, and get AI-powered answers using Google's Gemini 2.5 Flash model.

---

## ✨ Features

- 🔐 User registration and login with JWT authentication
- 📄 Upload PDF documents (each user sees only their own)
- 🤖 Ask questions about uploaded documents using Gemini AI (RAG pattern)
- ☁️ Documents backed up to Google Cloud Storage
- 🐳 Fully containerized with Docker
- ☸️ Kubernetes deployment with secrets management and load balancing

---

## 🏗️ Architecture

User → FastAPI (REST API)
↓
PDF Extraction (PyPDF2)
↓
Cloud Storage (GCP) ← backup
↓
Gemini 2.5 Flash (Vertex AI)
↓
Answer returned to user

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| API Framework | FastAPI |
| AI Model | Gemini 2.5 Flash (Vertex AI) |
| Cloud Storage | Google Cloud Storage |
| Authentication | JWT (python-jose + passlib bcrypt) |
| PDF Extraction | PyPDF2 |
| Containerization | Docker + Docker Compose |
| Orchestration | Kubernetes (Minikube locally, GKE for cloud) |

---

## 📁 Project Structure

llm-doc-qa/
│
├── app.py                  # Main entry point
├── routers/
│   ├── auth.py             # /auth/register, /auth/login
│   └── documents.py        # /upload, /ask, /documents
├── models/
│   └── schemas.py          # Pydantic request/response models
├── services/
│   ├── auth_service.py     # Password hashing, JWT logic
│   ├── pdf_service.py      # PDF text extraction
│   └── gemini_service.py   # Gemini AI integration
├── core/
│   ├── config.py           # Environment settings
│   └── state.py            # Shared in-memory storage
├── docker/
│   ├── Dockerfile          # Container build instructions
│   └── docker-compose.yml  # Local Docker setup
├── kubernetes/
│   ├── deployment.yaml     # K8s deployment (2 replicas)
│   ├── service.yaml        # K8s service (NodePort)
│   └── configmap.yaml      # Environment variables
├── run.sh                  # One command runner script
└── requirements.txt

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- GCP account with Vertex AI and Cloud Storage enabled
- Docker Desktop
- Minikube + kubectl (for Kubernetes)

### 1. Clone the repo
```bash
git clone https://github.com/Priyankjetani/llm-doc-qa.git
cd llm-doc-qa
```

### 2. Set up virtual environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment
Create a `.env` file:

GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
GCP_BUCKET=your-bucket-name
SECRET_KEY=your-secret-key

### 4. Run locally
```bash
uvicorn app:app --reload
# Visit http://127.0.0.1:8000/docs
```

---

## 🐳 Docker

```bash
# Build and start
./run.sh

# Stop
./run.sh stop

# Rebuild after code changes
./run.sh rebuild

# View logs
./run.sh logs
```

---

## ☸️ Kubernetes

```bash
# Start minikube
minikube start --driver=docker

# Create GCP key secret
kubectl create secret generic gcp-key-secret \
  --from-file=gcp-key.json=./gcp-key.json

# Deploy
./run.sh k8s-deploy

# Open in browser
./run.sh k8s-open

# Check status
./run.sh k8s-status

# View logs
./run.sh k8s-logs

# Stop
./run.sh k8s-stop
```

---

## 📡 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | No | Create account |
| POST | `/auth/login` | No | Login, get JWT token |
| POST | `/upload` | Yes | Upload a PDF |
| POST | `/ask` | Yes | Ask a question about a document |
| GET | `/documents` | Yes | List your uploaded documents |
| GET | `/docs` | No | Interactive API documentation |

---

## 💡 How it works (RAG Pattern)

1. User uploads a PDF → text is extracted and stored in memory
2. User asks a question
3. The document text + question is sent to Gemini as a prompt
4. Gemini reads the document and returns a precise answer
5. This pattern is called **RAG (Retrieval Augmented Generation)**

---

## 👤 Author
Priyank Jetani — [LinkedIn](https://www.linkedin.com/in/priyank-jetani) | [GitHub](https://github.com/Priyankjetani)