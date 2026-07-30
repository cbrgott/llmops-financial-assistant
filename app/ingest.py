from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore


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

print("\nCreating Qdrant vector database...")

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    path="qdrant_storage",
    collection_name="financial_documents"
)

print("Embeddings created and stored in Qdrant!")
vector_store.client.close()
print("Qdrant closed successfully!")