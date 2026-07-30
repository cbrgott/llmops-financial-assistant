from app.retriever import retrieve_documents, vector_store


question = "What are the company's climate goals?"

docs = retrieve_documents(question, k=3)


for i, doc in enumerate(docs):

    print("\n================")
    print(f"Result {i+1}")
    print(doc.page_content)

    print("\nMetadata:")
    print(doc.metadata)


vector_store.client.close()

print("\nQdrant closed successfully!")