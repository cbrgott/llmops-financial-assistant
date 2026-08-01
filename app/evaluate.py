import json

from app.rag import ask_rag
from app.evaluator import evaluate_answer


with open(
    "tests/evaluation_questions.json",
    "r",
    encoding="utf-8"
) as f:
    evaluation_data = json.load(f)


results = []

for item in evaluation_data:

    question = item["question"]

    expected_answer = item["expected_answer"]

    generated_answer = ask_rag(question)

    evaluation = evaluate_answer(
        question,
        expected_answer,
        generated_answer
    )

    results.append(
        {
            "question": question,
            "expected_answer": expected_answer,
            "generated_answer": generated_answer,
            "evaluation_score": evaluation["score"],
            "evaluation_reason": evaluation["reason"]
        }
    )


with open(
    "tests/evaluation_results.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False
    )


print("Evaluation completed.")