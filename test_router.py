from backend.router.query_router import handle_request


print("\n===== NORMAL RAG TEST =====\n")


response = handle_request(
    user_query="The vendor has unlimited liability."
)


print(response)



print("\n===== AGENTIC RAG TEST =====\n")


contract = """

The company may terminate this agreement at any time without notice.

The vendor shall be responsible for all damages, losses and claims without any limitation of liability.

"""


response = handle_request(
    user_query="Review this contract",
    document_text=contract
)


print(response)