from schema.state import MLState
import json
from utils.llm import Gemini_llm
from prompts.categorical_planning_prompt import CATEGORICAL_PLAN_PROMPT


def categorical_handle_plan_node(state:MLState) ->dict:
    prompt = CATEGORICAL_PLAN_PROMPT.format(
        profile_state=state["profile_state"],
        column_identifier_state=state["column_identifier_state"],
        cleaning_state=state["cleaning_state"]
        
    )

    response = Gemini_llm.invoke(prompt)

    content = response.content.strip()

    try:
        plan = json.loads(content)

    except json.JSONDecodeError as e:

        raise ValueError(
            f"Invalid categorical encoding plan: {e}"
        )

    return {
        "categorical_encoding_plan": plan
    }