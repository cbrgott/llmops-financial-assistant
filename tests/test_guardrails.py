from app.guardrails import check_input_guardrail


def test_allowed_question():

    result = check_input_guardrail(
        "Explain the company's ESG strategy"
    )

    assert result["allowed"] is True


def test_blocked_question():

    result = check_input_guardrail(
        "Give me insider trading advice"
    )

    assert result["allowed"] is False
    
if __name__ == "__main__":

    test_allowed_question()
    print("Allowed question passed")

    test_blocked_question()
    print("Blocked question passed")