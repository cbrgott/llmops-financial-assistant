from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import time

from app.pricing import (
    GPT5_MINI_INPUT_COST,
    GPT5_MINI_OUTPUT_COST
)

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

        print(response)

        latency = time.time() - start_time

        input_cost = (
            response.usage.input_tokens
            * GPT5_MINI_INPUT_COST
        )

        output_cost = (
            response.usage.output_tokens
            * GPT5_MINI_OUTPUT_COST
        )

        total_cost = input_cost + output_cost

        generation.update(
            output={
                "answer": response.output_text
            },
            metadata={
                "model": AZURE_OPENAI_DEPLOYMENT,
                "latency_seconds": round(latency, 3),
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.total_tokens,
                "estimated_cost_usd": round(total_cost, 8)
            }
        )

    return response.output_text