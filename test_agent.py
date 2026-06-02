from backend.agents.graph import build_graph


app = build_graph()


initial_state = {

    "document_text": """

    The company may terminate this agreement at any time without notice.

    The vendor shall be responsible for all damages, losses and claims without any limitation of liability.

    Both parties agree to protect confidential information.

    """,

    "clauses": [],

    "retrieved_context": {},

    "risks": [],

    "rewrites": [],

    "final_report": {}
}


result = app.invoke(
    initial_state
)


print(
    result["final_report"]
)