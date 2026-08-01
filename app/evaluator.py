from app.llm import ask_llm
import json

def evaluate_answer(
    question: str,
    expected_answer: str,
    generated_answer: str
):

    prompt = f"""
    You are an evaluator.

    Question:
    {question}

    Expected Answer:
    {expected_answer}

    Generated Answer:
    {generated_answer}

    Evaluate the generated answer.

    Score from 1 to 10 based on:
    - Correctness
    - Completeness
    - Relevance

    Return ONLY valid JSON:

    {{
        "score": number,
        "reason": "short explanation"
    }}

"""
    score = ask_llm(prompt)

    return json.loads(score)