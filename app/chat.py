import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT")
)

print(os.getenv("AZURE_OPENAI_ENDPOINT"))
print(os.getenv("AZURE_OPENAI_API_KEY"))

def ai_chat(user_message):

    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps people find information."
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    completion = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=messages,
        max_completion_tokens=800
    )

    return completion


print("Welcome! How can I help you today?")

while True:
    user_message = input(">> ")

    completion = ai_chat(user_message)

    print(
        completion.choices[0].message.content
    )