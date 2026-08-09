import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv


load_dotenv()

PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
AGENT_NAME = "financial-assistant-agent"


def run_agent(question: str) -> str:

    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
        allow_preview=True,
    )

    openai_client = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    response = openai_client.responses.create(
        input=question
    )

    # Check whether Foundry is asking approval
    for item in response.output:

        if item.type == "mcp_approval_request":

            response = openai_client.responses.create(
                previous_response_id=response.id,
                input=[
                    {
                        "type": "mcp_approval_response",
                        "approval_request_id": item.id,
                        "approve": True,
                    }
                ],
            )

            break

    return response.output_text