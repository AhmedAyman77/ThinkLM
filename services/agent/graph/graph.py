from langgraph.graph import StateGraph, END
from graph.nodes import AgentState, classify_intent, route_intent
from agents.rag import rag_agent
from agents.summarize import summarize_agent
from agents.translate import translate_agent
from agents.direct import direct_agent


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_intent)
    graph.add_node("RAG_QUERY", rag_agent)
    graph.add_node("SUMMARIZE", summarize_agent)
    graph.add_node("TRANSLATE", translate_agent)
    graph.add_node("DIRECT_LLM", direct_agent)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        route_intent,
        {
            "RAG_QUERY": "RAG_QUERY",
            "SUMMARIZE": "SUMMARIZE",
            "TRANSLATE": "TRANSLATE",
            "DIRECT_LLM": "DIRECT_LLM",
        }
    )

    graph.add_edge("RAG_QUERY", END)
    graph.add_edge("SUMMARIZE", END)
    graph.add_edge("TRANSLATE", END)
    graph.add_edge("DIRECT_LLM", END)

    return graph.compile()


agent_graph = build_graph()