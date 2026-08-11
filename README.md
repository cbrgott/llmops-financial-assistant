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

Create the virtual environment:

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

Open:

```text
http://localhost:8000/docs
```

---

## 2. Docker Compose

Build and start the full local stack:

```powershell
docker compose up --build
```

Or run in the background:

```powershell
docker compose up -d --build
```

Check containers:

```powershell
docker compose ps -a
```

Expected services:

```text
financial-assistant-api      Up
financial-assistant-ingest   Exited (0)
qdrant                       Up
```

Stop the stack:

```powershell
docker compose down
```

Docker Compose runs:

```text
Qdrant
 ↓
Ingestion container
 ↓
API container
```

The API and ingestion containers use:

```text
QDRANT_URL=http://qdrant:6333
```

---

## 3. Azure Deployment

Azure deployment is automated through GitHub Actions.

Commit and push:

```powershell
git add .
git commit -m "Update application"
git push origin master
```

The pipeline runs:

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
Push to GHCR
 ↓
Deploy to Azure Container Apps
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

Run the Azure ingestion job when the vector database needs to be rebuilt:

```powershell
az containerapp job start `
  --name financial-assistant-ingest `
  --resource-group demo-container
```

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

## Author

**Cristhian Balta**