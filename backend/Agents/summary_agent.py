from utils.llm import Gemini_llm
from prompts.summary_agent_prompt import SUMMARY_PROMPT
from schema.state import MLState
from schema.state import SummaryState


def summary_agent(state: MLState) -> dict:
    """Analyze profile state and generate dataset summary."""

    prompt = SUMMARY_PROMPT.format(
        profile_state=state["profile_state"]
    )

    structured_llm = Gemini_llm.with_structured_output(
        SummaryState
    )

    response = structured_llm.invoke(prompt)

    return {
        "summary_state": response.model_dump()
    }