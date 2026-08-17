import json

from utils.llm import Groq_llm
from prompts.cleaning_prompt import CLEANING_PROMPT
from schema.state import MLState


def cleaning_agent(state: MLState) -> dict:

    prompt = CLEANING_PROMPT.format(
        file_path=state["file_path"],
        profile_state=state["profile_state"],
        summary_state=state["summary_state"],
        column_identifier_state=state["column_identifier_state"],
        selected_columns_to_remove = state["selected_columns_to_remove"]

    )

    response = Groq_llm.invoke(prompt)

    cleaning_plan = json.loads(response.content)

    return {
        "cleaning_plan": cleaning_plan
    }