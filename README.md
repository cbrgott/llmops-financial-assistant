# LLMOps & Agentic AI Financial Assistant

An end-to-end **LLMOps and agentic AI Financial Assistant** built with RAG, Azure AI Foundry, MCP, Qdrant, FastAPI, Langfuse, Docker, and CI/CD.

The system answers questions about financial and ESG documents using Retrieval-Augmented Generation.

---

## Architecture

### Ingestion

```text
PDF
 ↓
PyPDFLoader
 ↓
Chunking
 ↓
Hugging Face Embeddings
 ↓
Qdrant
```

### RAG

```text
User Question
 ↓
FastAPI
 ↓
Guardrail
 ↓
Retriever
 ↓
Qdrant
 ↓
Top 3 Chunks
 ↓
Prompt
 ↓
Azure OpenAI
 ↓
Answer
```

### Agent

```text
User Question
 ↓
FastAPI /agent
 ↓
Azure AI Foundry Agent
 ↓
MCP Tool
 ↓
Qdrant Retrieval
 ↓
Agent Answer
```

---

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python |
| API | FastAPI |
| Web Server | Uvicorn |
| LLM | Azure OpenAI |
| Agent | Azure AI Foundry Agent |
| Embeddings | Hugging Face `all-MiniLM-L6-v2` |
| Vector Database | Qdrant |
| RAG | LangChain |
| MCP | MCP Server |
| Observability | Langfuse |
| Testing | Pytest |
| Containers | Docker |
| CI/CD | GitHub Actions |
| Image Registry | GHCR |
| Cloud | Azure Container Apps |

---

## Project Structure

```text
llmops-financial-assistant/
│
├── app/
│   ├── agent.py
│   ├── api.py
│   ├── config.py
│   ├── evaluate.py
│   ├── evaluator.py
│   ├── guardrails.py
│   ├── ingest.py
│   ├── llm.py
│   ├── mcp_server.py
│   ├── observability.py
│   ├── rag.py
│   ├── retriever.py
│   ├── schemas.py
│   └── tools.py
│
├── data/
├── tests/
├── .github/workflows/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

---

# Run the Project

The project can run in three ways:

1. Local Python
2. Docker Compose
3. Azure

---

## 1. Local Python

Create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Configure `.env`:

```env
QDRANT_URL=http://localhost:6333
```

Start Qdrant:

```powershell
docker run -d `
  --name qdrant `
  -p 6333:6333 `
  -p 6334:6334 `
  qdrant/qdrant
```

Run ingestion:

```powershell
python app/ingest.py
```

Start the API:

```powershell
uvicorn app.api:app --reload
```

Access the API:

```text
API:     http://localhost:8000
Swagger: http://localhost:8000/docs
Health:  http://localhost:8000/health
```

---

## 2. Docker Compose

Build and start the complete local stack:

```powershell
docker compose up --build
```

Docker Compose runs:

```text
Qdrant
 ↓
Ingestion container
 ↓
API container
```

Check the containers:

```powershell
docker compose ps -a
```

Expected services:

```text
financial-assistant-api      Up
financial-assistant-ingest   Exited (0)
qdrant                       Up
```

`financial-assistant-ingest` exits after successfully populating Qdrant.

Inside the Docker network, the API and ingestion containers connect to Qdrant using:

```text
QDRANT_URL=http://qdrant:6333
```

Access the application from the host:

```text
API:              http://localhost:8000
Swagger:          http://localhost:8000/docs
Health:           http://localhost:8000/health
Qdrant Dashboard: http://localhost:6333/dashboard
```

Stop the stack:

```powershell
docker compose down
```

---

## 3. Azure Deployment

Azure deployment is automated through GitHub Actions.

Commit and push to `master`:

```powershell
git add .
git commit -m "Update application"
git push origin master
```

The deployment pipeline runs:

```text
Push to master
 ↓
CI
 ↓
Tests
 ↓
CD
 ↓
Build Docker Image
 ↓
Tag Image with Git SHA
 ↓
Push to GHCR
 ↓
Deploy to Azure Container Apps
```

Get the public API hostname:

```powershell
az containerapp show `
  --name financial-assistant-api `
  --resource-group demo-container `
  --query "properties.configuration.ingress.fqdn" `
  -o tsv
```

Access the deployed application using the returned hostname:

```text
API:     https://<azure-api-fqdn>
Swagger: https://<azure-api-fqdn>/docs
Health:  https://<azure-api-fqdn>/health
```

Check API revisions:

```powershell
az containerapp revision list `
  --name financial-assistant-api `
  --resource-group demo-container `
  -o table
```

Check the currently deployed image:

```powershell
az containerapp revision show `
  --name financial-assistant-api `
  --resource-group demo-container `
  --revision <revision-name> `
  --query "properties.template.containers[0].image" `
  -o tsv
```

Check the current Git commit:

```powershell
git rev-parse HEAD
```

The Git SHA should match the Docker image tag deployed in Azure.

Run the Azure ingestion job when the vector database needs to be initially populated or rebuilt:

```powershell
az containerapp job start `
  --name financial-assistant-ingest `
  --resource-group demo-container
```

The ingestion job is not required for normal user requests.

---

## API Endpoints

```text
GET  /
GET  /health
POST /ask
POST /agent
```

`/ask` uses the custom RAG pipeline.

`/agent` uses the Azure AI Foundry Agent and MCP tools.

---

## Observability

Langfuse tracks:

- RAG requests
- Retrieved documents
- Source pages
- Context size
- LLM latency
- Token usage
- Estimated cost
- Generated answers
- Evaluation scores

---

## Evaluation

The project includes offline evaluation using:

```text
Question
+
Expected Answer
+
Generated Answer
 ↓
LLM-as-a-Judge
 ↓
Score + Reason
```

Evaluation results are stored locally and sent to Langfuse.

---

## CI

The CI pipeline:

```text
Push / Pull Request
 ↓
Temporary GitHub Runner
 ↓
Temporary Qdrant
 ↓
Ingest Documents
 ↓
Run Pytest
 ↓
Pass / Fail
```

---

## CD

The CD pipeline:

```text
Push to master
 ↓
Build financial-assistant Docker image
 ↓
Tag with Git SHA
 ↓
Push to GHCR
 ↓
Login to Azure
 ↓
Update financial-assistant-api
 ↓
Update financial-assistant-mcp
 ↓
New Azure Container App revisions
```

---

## Azure Architecture

```text
Azure
│
├── Azure AI Foundry
│   └── Financial Assistant Agent
│
├── Azure OpenAI
│   └── GPT-5-mini
│
├── Azure Container Apps
│   ├── financial-assistant-api
│   ├── financial-assistant-mcp
│   └── qdrant
│
└── Azure Container Apps Job
    └── financial-assistant-ingest
```

---

## Deployment Summary

```text
LOCAL PYTHON
Python + Local Qdrant
        ↓
http://localhost:8000


DOCKER COMPOSE
API + Ingest + Qdrant containers
        ↓
http://localhost:8000


AZURE
Git Push
   ↓
CI/CD
   ↓
GHCR
   ↓
Azure Container Apps
   ↓
https://<azure-api-fqdn>
```

---

## Author

**Cristhian Balta**