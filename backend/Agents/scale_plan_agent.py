from utils.llm import Groq_llm
from schema.state import MLState
from prompts.scale_plan_prompt import SCALING_PLAN_PROMPT
import json

def scaled_plan_node(state: MLState) -> dict:


 prompt = SCALING_PLAN_PROMPT.format(
    profile_state=state["profile_state"],
    column_identifier_state=state["column_identifier_state"],
    categorical_encoding_plan=state["categorical_encoding_plan"]
)

 response = Groq_llm.invoke(prompt)

 content = response.content

 if isinstance(content, list):
    content = "".join(
        part.get("text", "")
        if isinstance(part, dict)
        else str(part)
        for part in content
    )

 content = content.strip()

 try:
    plan = json.loads(content)

 except json.JSONDecodeError as e:
    raise ValueError(
        f"Invalid scaling plan: {e}"
    )

 return {
    "scaling_plan": plan
}

