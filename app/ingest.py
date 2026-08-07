from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
import os

# -----------------------------
# 1. Load PDF
# -----------------------------

pdf_path = Path("data") / "2021ESG.pdf"

loader = PyPDFLoader(str(pdf_path))

documents = loader.load()

print(f"Pages loaded : {len(documents)}")


# -----------------------------
# 2. Split documents into chunks
# -----------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print(f"Chunks created: {len(chunks)}")


print("\nFirst chunk:")
print(chunks[0].page_content)

print("\nChunk metadata:")
print(chunks[0].metadata)


# -----------------------------
# 3. Create embedding model
# -----------------------------

print("\nLoading embedding model...")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded!")


# -----------------------------
# 4. Store embeddings in Qdrant
# -----------------------------

from qdrant_client import QdrantClient
import httpx

QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://localhost:6333"
)

print("QDRANT_URL =", QDRANT_URL)

# Direct HTTP test
print("Testing Qdrant URL:", QDRANT_URL)

try:
    response = httpx.get(
        f"{QDRANT_URL}/collections",
        timeout=30
    )
    print("HTTPX status:", response.status_code)
    print("HTTPX response:", response.text[:1000])
except Exception as e:
    print("HTTPX connectivity error:", repr(e))

# Qdrant client test
client = QdrantClient(
    url=QDRANT_URL,
    timeout=120,
    prefer_grpc=False
)

print("Testing Qdrant connection...")
print(client.get_collections())
print("Qdrant connection OK!")

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url=QDRANT_URL,
    collection_name="financial_documents",
    timeout=120
)

print("Embeddings created and stored in Qdrant!")

client.close()

print("Qdrant closed successfully!")