from app.retriever import retrieve_documents
from app.llm import ask_llm
from app.observability import langfuse
from app.logger import logger

def ask_rag(question: str):

    logger.info(
        f"Received question: {question}"
    )

    with langfuse.start_as_current_observation(
        name="rag-request",
        input={
            "question": question
        }
    ) as trace:

        # 1. Retrieve relevant documents
        with langfuse.start_as_current_observation(
            name="retrieve-documents"
        ) as retrieval_span:

            documents = retrieve_documents(
                question,
                k=3
            )

            logger.info(
                f"Retrieved documents: {len(documents)}"
            )

            retrieval_span.update(
                output={
                    "documents_found": len(documents),
                    "sources": [
                        doc.metadata.get("source")
                        for doc in documents
                    ],
                    "pages": [
                        doc.metadata.get("page")
                        for doc in documents
                    ]
                }
            )


        # 2. Build context
        with langfuse.start_as_current_observation(
            name="build-context"
        ) as context_span:

            context = "\n\n".join(
                doc.page_content
                for doc in documents
            )

            logger.info(f"Context lengh: {len(context)} characters")

            context_span.update(
                output={
                    "context_length_characters": len(context),
                    "chunks_used": len(documents)
                }
            )


        # 3. Create prompt
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


        trace.update(
            output={
                "answer": answer
            }
        )


    return answer

logger.info(
    "Response generated successfully"
)