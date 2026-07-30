from app.rag import ask_rag


question = "What is the purpose of this ESG and Climate Change Report?"

answer = ask_rag(question)


print("\nFinal answer:")
print(answer)