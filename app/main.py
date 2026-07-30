from app.llm import ask_llm


if __name__ == "__main__":

    answer = ask_llm(
        "Explain what a balance sheet is in simple terms."
    )

    print(answer)