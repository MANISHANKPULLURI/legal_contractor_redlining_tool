from langgraph.graph import StateGraph, END

from backend.agents.state import LegalReviewState

from backend.agents.parser_agent import parser_agent
from backend.agents.retrieval_agent import retrieval_agent
from backend.agents.relevance_agent import relevance_agent
from backend.agents.risk_agent import risk_agent
from backend.agents.rewrite_agent import rewrite_agent
from backend.agents.redline_agent import redline_agent



def build_graph():


    graph = StateGraph(
        LegalReviewState
    )


    # add agent nodes

    graph.add_node(
        "parser",
        parser_agent
    )

    graph.add_node(
    "relevance",
    relevance_agent
)


    graph.add_node(
        "retrieval",
        retrieval_agent
    )


    graph.add_node(
        "risk",
        risk_agent
    )


    graph.add_node(
        "rewrite",
        rewrite_agent
    )


    graph.add_node(
        "redline",
        redline_agent
    )



    # define flow

    graph.set_entry_point(
        "parser"
    )


    graph.add_edge(
    "parser",
    "relevance"
)


    graph.add_edge(
    "relevance",
    "retrieval"
)


    graph.add_edge(
        "retrieval",
        "risk"
    )


    graph.add_edge(
        "risk",
        "rewrite"
    )


    graph.add_edge(
        "rewrite",
        "redline"
    )


    graph.add_edge(
        "redline",
        END
    )


    return graph.compile()