from backend.agents.graph import build_graph
from backend.review.review_chain import review_clause


# load graph once
agent_app = build_graph()


def handle_request(
    user_query,
    document_text=None
):


    # CASE 1:
    # User uploaded document
    # use Agentic RAG

    if document_text:


        initial_state = {

            "document_text": document_text,

            "clauses": [],

            "retrieved_context": {},

            "risks": [],

            "rewrites": [],

            "final_report": {}

        }


        result = agent_app.invoke(
            initial_state
        )


        return result["final_report"]



    # CASE 2:
    # Only text question
    # use normal RAG

    else:


        result = review_clause(
            user_query
        )


        return result