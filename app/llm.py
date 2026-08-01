from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import time

from app.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT
)

from app.observability import langfuse

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)


client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=token_provider
)


def ask_llm(prompt: str):

    start_time = time.time()

    with langfuse.start_as_current_observation(
        name="llm-generation"
    ) as generation:

        response = client.responses.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            input=prompt
        )

        latency = time.time() - start_time

        generation.update(
            output={
                "answer": response.output_text
            },
            metadata={
                "model": AZURE_OPENAI_DEPLOYMENT,
                "latency_seconds": round(latency, 3)
            }
        )

    return response.output_text