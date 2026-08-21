from langgraph.graph import StateGraph, START, END
from schema.state import MLState
from langgraph.types import interrupt
from Agents.profile_extractor_agent import profile_extractor_node
from Agents.summary_agent import summary_agent
from Agents.cleaning_agent import cleaning_plan_agent
from Agents.cleaning_executor_node import cleaning_executor
from Agents.column_identifier_agent import column_identifier_node
from Agents.Categorical_plan_agent import categorical_handle_plan_node
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

def human_column_selection_node(state:MLState):
    column_identifier = state.get("column_identifier_state", {})
    columns = column_identifier.get("columns", [])

    user_input = interrupt({
        "type": "column_selection",
        "message":"Select columns you want to remove",
        "columns": columns
    })

    return {
        "selected_columns_to_remove": user_input
    }

def build_ml_graph():

    graph = StateGraph(MLState)

    # graph.add_node("profile_report", profiling_node)
    graph.add_node("profile_extractor", profile_extractor_node)
    graph.add_node("column_identifier", column_identifier_node)
    graph.add_node("human_column_selection",human_column_selection_node
    )
    graph.add_node("summary_agent", summary_agent)
    graph.add_node("cleaning_agent",cleaning_plan_agent)
    graph.add_node("cleaning_executor",cleaning_executor)

    # graph.add_edge(START, "profile_report")
    # graph.add_edge("profile_report", END)
    graph.add_edge(START, "profile_extractor")
    graph.add_edge("profile_extractor", "summary_agent")
    graph.add_edge("summary_agent", "column_identifier") # make cleaned plan for dataset 
    graph.add_edge("column_identifier","human_column_selection")
    graph.add_edge("human_column_selection","cleaning_agent")
    graph.add_edge("cleaning_agent","cleaning_executor")
    graph.add_edge("cleaning_executor",END)

    return graph.compile(checkpointer=checkpointer)