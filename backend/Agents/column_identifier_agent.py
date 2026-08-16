import json

from utils.llm import Groq_llm
from prompts.column_identifier_prompt import COLUMN_IDENTIFIER_PROMPT

from schema.state import MLState
from schema.state import ColumnIdentifierState


def column_identifier_node(state: MLState) -> dict:

    prompt = COLUMN_IDENTIFIER_PROMPT.format(
        profile_state=state["profile_state"]
    )

    response = Groq_llm.invoke(prompt)

    result = json.loads(response.content)

    validated = ColumnIdentifierState.model_validate(result)

    return {
        "column_identifier_state": validated.model_dump()
    }