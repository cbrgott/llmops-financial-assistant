from app.rag import ask_rag

def test_rag_generates_answer():

    question = "What is the purpose of this ESG and Climate Change Report?"

    answer = ask_rag(question)

    print("\nFinal answer:")
    print(answer)

if __name__ == "__main__":
    test_rag_generates_answer()