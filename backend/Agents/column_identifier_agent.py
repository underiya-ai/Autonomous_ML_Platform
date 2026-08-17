import json

from utils.llm import Groq_llm
from prompts.column_identifier_prompt import COLUMN_IDENTIFIER_PROMPT

from schema.state import MLState
from schema.state import ColumnIdentifierState


def column_identifier_node(state: MLState) -> dict:

    prompt = COLUMN_IDENTIFIER_PROMPT.format(
        profile_state=state["profile_state"],
        summary_state=state["summary_state"]
    )

    response = Groq_llm.invoke(prompt)

    result = json.loads(response.content)

    # LLM sometimes returns a direct list
    if isinstance(result, list):
        result = {
            "columns": result,
            "important_warnings": [],
            "summary": "Columns identified successfully."
        }

    validated = ColumnIdentifierState.model_validate(result)

    return {
        "column_identifier_state": validated.model_dump()
    }