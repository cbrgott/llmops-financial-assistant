from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
import os


# -----------------------------
# Load embedding model
# -----------------------------

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------
# Connect to existing Qdrant database
# -----------------------------

QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://localhost:6333"
)

print(f"QDRANT_URL = {QDRANT_URL}")
vector_store = QdrantVectorStore.from_existing_collection(
    collection_name="financial_documents",
    url=QDRANT_URL,
    embedding=embedding_model
)




# -----------------------------
# Retrieval function
# -----------------------------

def retrieve_documents(question: str, k: int = 3):
    """
    Retrieve the most relevant document chunks from Qdrant.

    Args:
        question: User question.
        k: Number of chunks to retrieve.

    Returns:
        List of relevant documents.
    """

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results