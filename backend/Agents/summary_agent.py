from utils.llm import llm
from prompts.summary_agent_prompt import SUMMARY_PROMPT
from schema.state import MLState



def summary_agent(state:MLState) -> dict:
    """Analyze and give  all over summary of data"""

    prompt = SUMMARY_PROMPT.format(
        profile_state = state['profile_state']
    )

    response = llm.invoke(prompt)

    summary_state = response.content

    return {
        "summary_state":summary_state
    }




