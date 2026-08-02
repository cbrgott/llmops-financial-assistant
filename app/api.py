from fastapi import FastAPI, HTTPException
from app.rag import ask_rag
from app.schemas import QuestionRequest, AnswerResponse
from app.guardrails import check_input_guardrail
from app.observability import langfuse
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

        with langfuse.start_as_current_observation(
            name="guardrail-check",
            input={
                "question": request.question
            }
        ) as guardrail_span:

            guardrail_result = check_input_guardrail(
                request.question
            )

            guardrail_span.update(
                output=guardrail_result
        )

        if not guardrail_result["allowed"]:

            logger.warning(
                "Blocked request: %s",
                request.question
            )

            return AnswerResponse(
                answer=guardrail_result["reason"]
            )


        result  = ask_rag(request.question)
        logger.info("RAG response generated successfully")

        return AnswerResponse(answer=result["answer"])

    except Exception as e:
        logger.error(
            "RAG  request failed: %s",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail="RAG service unavailable"
        )