from utils.llm import llm

from prompts.cleaning_prompt import CLEANING_PROMPT

from schema.state import MLState

from schema.state import CleaningPlanState


def cleaning_agent(state: MLState) -> dict:
    """
    Analyze dataset profile and summary
    and generate a cleaning plan.
    """

    prompt = CLEANING_PROMPT.format(

        file_path=state["file_path"],

        profile_state=state["profile_state"],

        summary_state=state["summary_state"]
    )

    structured_llm = llm.with_structured_output(CleaningPlanState)

    response = structured_llm.invoke(prompt)

    return {
        "cleaning_plan": response.model_dump()
    }