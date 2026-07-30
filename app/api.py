from fastapi import FastAPI, HTTPException
from app.rag import ask_rag
from app.schemas import QuestionRequest, AnswerResponse
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="LLMOps Financial Assistant",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "LLMOps Financial Assistant API is running!"}


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):

    logger.info(
        "Received question: %s",
        request.question
    )

    try:
        answer = ask_rag(request.question)

        logger.info("RAG response generated successfully")

        return AnswerResponse(answer=answer)

    except Exception as e:
        logger.error(
            "RAG  request failed: %s",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail="RAG service unavailable"
        )