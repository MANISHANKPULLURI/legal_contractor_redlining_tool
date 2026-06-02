from typing import TypedDict, List, Dict, Any


class LegalReviewState(TypedDict):


    user_query: str
    # original user instruction/query


    chat_history: List[Dict[str, str]]
    # conversation memory
    # example:
    # [
    #   {
    #      "role":"user",
    #      "content":"review NDA"
    #   },
    #   {
    #      "role":"assistant",
    #      "content":"Risk 1..."
    #   }
    # ]



    document_text: str
    # uploaded contract text



    clauses: List[str]
    # parser_agent.py output



    retrieved_context: Dict[str, Any]
    # retrieval_agent.py output



    risks: List[Dict[str, Any]]
    # risk_agent.py output



    rewrites: List[Dict[str, Any]]
    # rewrite_agent.py output



    final_report: Dict[str, Any]
    # redline_agent.py output