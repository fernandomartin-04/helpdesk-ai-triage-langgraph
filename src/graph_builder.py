from langgraph.graph import StateGraph, END

from src.graph_state import TicketState
from src.graph_nodes import classify_node, summarize_node, generate_reply_node


def build_graph():
    """
    Crea y compila el grafo:
    classify -> summarize -> generate_reply -> END
    """
    graph = StateGraph(TicketState)

    # registrar nodos
    graph.add_node("classify", classify_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("generate_reply", generate_reply_node)

    # definir punto de entrada
    graph.set_entry_point("classify")

    # definir flujo (edges)
    graph.add_edge("classify", "summarize")
    graph.add_edge("summarize", "generate_reply")
    graph.add_edge("generate_reply", END)

    # compilar (convierte la definición en algo ejecutable)
    return graph.compile()
