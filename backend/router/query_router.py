from backend.agents.graph import build_graph

from backend.review.review_chain import review_clause
from backend.review.qa_chain import answer_question

from backend.memory.chat_memory import (
    add_message,
    get_history
)



agent_app = build_graph()



def handle_request(
        user_query,
        document_text=None,
        session_id="default"
):


    # -------------------------
    # Load memory
    # -------------------------

    history = get_history(
        session_id
    )



    add_message(
        session_id,
        "user",
        user_query
    )






    # ===================================
    # FILE UPLOAD → AGENTIC CONTRACT RAG
    # ===================================


    if document_text:


        initial_state = {


            "user_query":
            user_query,


            "document_text":
            document_text,


            "chat_history":
            history,


            "clauses":
            [],


            "retrieved_context":
            {},


            "risks":
            [],


            "rewrites":
            [],


            "final_report":
            {}

        }




        result = agent_app.invoke(

            initial_state

        )




        final_report = result[

            "final_report"

        ]




        add_message(

            session_id,

            "assistant",

            str(final_report)

        )



        return final_report







    # ===================================
    # TEXT CHAT ROUTER
    # ===================================


    query = user_query.lower().strip()





    review_keywords = [


        "review this clause",

        "analyze this clause",

        "analyse this clause",

        "check this clause",

        "find risk in this clause",

        "find risks in this clause",

        "rewrite this clause",

        "improve this clause",

        "fix this clause",

        "make this clause safer"

    ]






    is_review_request = any(


        keyword in query


        for keyword in review_keywords


    )








    # Add conversation memory


    memory_query = f"""

Previous conversation:

{history}



Current user request:

{user_query}

"""







    # --------------------------
    # Clause review only
    # when explicitly requested
    # --------------------------


    if is_review_request:



        response = review_clause(

            memory_query

        )






    # --------------------------
    # Default:
    # Normal Legal RAG
    # --------------------------


    else:



        response = answer_question(

            memory_query

        )









    add_message(

        session_id,

        "assistant",

        str(response)

    )





    return response