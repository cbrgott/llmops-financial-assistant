from app.retriever import retrieve_documents


def financial_search(query: str) -> str:
    """
    Search the company's financial and ESG documents.

    Use this tool when the user asks about information that may be
    contained in the indexed financial documents.
    """

    docs = retrieve_documents(query, k=3)

    if not docs:
        return "No relevant financial documents were found."

    return "\n\n".join(
        f"Document {i + 1}:\n{doc.page_content}"
        for i, doc in enumerate(docs)
    )