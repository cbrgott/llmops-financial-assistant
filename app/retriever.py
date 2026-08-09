from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os
import requests

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://localhost:6333"
)

COLLECTION_NAME = "financial_documents"

print(f"QDRANT_URL = {QDRANT_URL}")


def retrieve_documents(question: str, k: int = 3):
    query_vector = embedding_model.embed_query(question)

    response = requests.post(
        f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/search",
        json={
            "vector": query_vector,
            "limit": k,
            "with_payload": True
        },
        timeout=30
    )

    response.raise_for_status()

    results = response.json()["result"]

    documents = []

    for result in results:
        payload = result["payload"]

        documents.append(
            Document(
                page_content=payload["page_content"],
                metadata=payload.get("metadata", {})
            )
        )

    return documents