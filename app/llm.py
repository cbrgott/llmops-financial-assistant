from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from app.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT
)


token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)


client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=token_provider
)


def ask_llm(prompt: str):

    response = client.responses.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        input=prompt
    )

    return response.output_text