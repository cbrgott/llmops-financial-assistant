BLOCKED_PATTERNS = [
    "insider trading",
    "guaranteed profit",
    "make me rich",
    "secret stock tip",
    "manipulate earnings"
]


def check_input_guardrail(question: str):

    question_lower = question.lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in question_lower:
            return {
                "allowed": False,
                "reason": "Request violates financial safety guidelines."
            }

    return {
        "allowed": True,
        "reason": None
    }
