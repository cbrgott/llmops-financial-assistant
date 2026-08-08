from pathlib import Path
import os
import requests

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


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
# 4. Qdrant configuration
# -----------------------------

QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://localhost:6333"
)

COLLECTION_NAME = "financial_documents"

print("QDRANT_URL =", QDRANT_URL)


# -----------------------------
# 5. Test Qdrant connection
# -----------------------------

print("Testing Qdrant connection...")

try:
    response = requests.get(
        QDRANT_URL,
        timeout=30
    )

    print("Qdrant HTTP status:", response.status_code)
    print("Qdrant response:", response.text[:500])

    response.raise_for_status()

except Exception as e:
    print("Qdrant connectivity error:", repr(e))
    raise


# -----------------------------
# 6. Recreate collection
# -----------------------------

print(f"Deleting existing Qdrant collection: {COLLECTION_NAME}")

try:
    response = requests.delete(
        f"{QDRANT_URL}/collections/{COLLECTION_NAME}",
        timeout=30
    )

    print("Collection deletion status:", response.status_code)
    print("Collection deletion response:", response.text[:500])

    if response.status_code not in [200, 404]:
        response.raise_for_status()

except Exception as e:
    print("Collection deletion error:", repr(e))
    raise


print(f"Creating fresh Qdrant collection: {COLLECTION_NAME}")

try:
    response = requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION_NAME}",
        json={
            "vectors": {
                "size": 384,
                "distance": "Cosine"
            }
        },
        timeout=30
    )

    print("Collection creation status:", response.status_code)
    print("Collection creation response:", response.text[:500])

    response.raise_for_status()

    print("Collection created successfully!")

except Exception as e:
    print("Collection creation error:", repr(e))
    raise

# -----------------------------
# 7. Create embeddings
# -----------------------------

print(f"Creating embeddings for {len(chunks)} chunks...")

texts = [chunk.page_content for chunk in chunks]

embeddings = embedding_model.embed_documents(texts)

print(f"Embeddings created: {len(embeddings)}")
print(f"Embedding dimension: {len(embeddings[0])}")


# -----------------------------
# 8. Upload vectors to Qdrant
# -----------------------------

print("Uploading vectors to Qdrant...")

batch_size = 50

for start in range(0, len(chunks), batch_size):

    end = min(start + batch_size, len(chunks))

    points = []

    for i in range(start, end):

        points.append({
            "id": i,
            "vector": embeddings[i],
            "payload": {
                "page_content": chunks[i].page_content,
                "metadata": chunks[i].metadata
            }
        })

    response = requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points",
        params={"wait": "true"},
        json={
            "points": points
        },
        timeout=120
    )

    print(
        f"Uploaded chunks {start + 1}-{end}: "
        f"HTTP {response.status_code}"
    )

    print(response.text[:300])

    response.raise_for_status()


print("Embeddings created and stored in Qdrant!")
print("Ingestion completed successfully!")