from app.retriever import retrieve_documents
from app.llm import ask_llm


def ask_rag(question: str):

    # 1. Retrieve relevant documents
    documents = retrieve_documents(
        question,
        k=3
    )


    # 2. Build context from retrieved chunks
    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )


    # 3. Create RAG prompt
    prompt = f"""
You are a financial assistant.

Answer the user's question using only the context below.

If the context does not contain the answer,
say that you do not have enough information.

Context:
{context}

Question:
{question}
"""


    # 4. Call Azure GPT-5-mini
    answer = ask_llm(prompt)


    return answer