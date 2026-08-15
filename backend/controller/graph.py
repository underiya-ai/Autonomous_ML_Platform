from langgraph.graph import StateGraph, START, END

from schema.state import MLState

# from Agents.profiling_report_agent import profiling_node
from Agents.profile_extractor_agent import profile_extractor_node
from Agents.summary_agent import summary_agent
from Agents.cleaning_agent import cleaning_agent
from Agents.cleaning_executor_node import cleaning_executor


def build_ml_graph():

    graph = StateGraph(MLState)

    # graph.add_node("profile_report", profiling_node)
    graph.add_node("profile_extractor", profile_extractor_node)
    graph.add_node("summary_agent", summary_agent)
    graph.add_node("cleaning_agent",cleaning_agent)
    graph.add_node("cleaning_executor",cleaning_executor)

    # graph.add_edge(START, "profile_report")
    # graph.add_edge("profile_report", END)
    graph.add_edge(START, "profile_extractor")
    graph.add_edge("profile_extractor", "summary_agent")
    graph.add_edge("summary_agent", "cleaning_agent")   # make cleaned plan for dataset 
    graph.add_edge("cleaning_agent","cleaning_executor")
    graph.add_edge("cleaning_executor",END)

    return graph.compile()