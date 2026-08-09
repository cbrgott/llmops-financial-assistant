from app.retriever import retrieve_documents


def test_retriever_returns_documents():
    question = "What are the company's climate goals?"

    docs = retrieve_documents(question, k=3)

    assert len(docs) > 0

    for i, doc in enumerate(docs):
        print("\n================")
        print(f"Result {i+1}")
        print(doc.page_content)

        print("\nMetadata:")
        print(doc.metadata)


if __name__ == "__main__":
    test_retriever_returns_documents()