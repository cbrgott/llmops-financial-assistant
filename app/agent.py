import json
import os

from openai import OpenAI
from azure.identity import (
    DefaultAzureCredential,
    get_bearer_token_provider,
)
from dotenv import load_dotenv

from app.tools import financial_search


# ---------------------------------
# Load environment variables
# ---------------------------------

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
MODEL_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]


# ---------------------------------
# Azure authentication
# ---------------------------------

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default",
)


# ---------------------------------
# OpenAI client
# ---------------------------------

client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=token_provider,
)


# ---------------------------------
# Agent
# ---------------------------------

def run_agent(question: str) -> str:

    response = client.responses.create(
        model=MODEL_DEPLOYMENT,

        instructions=(
            "You are a financial assistant for Tongaat Hulett. "
            "The indexed documents belong to Tongaat Hulett. "
            "Whenever the user asks about 'the company', Tongaat Hulett, "
            "ESG, sustainability, climate, governance, risk, strategy, "
            "financial information, or company-specific facts, "
            "you MUST use the financial_search tool before answering."
        ),

        input=question,

        tools=[
            {
                "type": "function",
                "name": "financial_search",
                "description": (
                    "Search Tongaat Hulett's indexed financial and ESG documents. "
                    "Always use this tool for company-specific questions."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": (
                                "The question to search for in "
                                "Tongaat Hulett's documents."
                            ),
                        }
                    },
                    "required": ["query"],
                    "additionalProperties": False,
                },
            }
        ],
    )

    # ---------------------------------
    # Handle tool call
    # ---------------------------------

    for item in response.output:

        if (
            item.type == "function_call"
            and item.name == "financial_search"
        ):

            arguments = json.loads(item.arguments)

            result = financial_search(
                arguments["query"]
            )

            # Send tool result back to the model
            final_response = client.responses.create(
                model=MODEL_DEPLOYMENT,
                previous_response_id=response.id,
                input=[
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": result,
                    }
                ],
            )

            return final_response.output_text

    # Agent decided that no tool was necessary
    return response.output_text