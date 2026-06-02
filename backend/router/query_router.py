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


    # Load previous chat

    history = get_history(session_id)



    # Save user message

    add_message(
        session_id,
        "user",
        user_query
    )



    # --------------------------------
    # File uploaded → Agentic RAG
    # --------------------------------


    if document_text:


        initial_state = {


            "user_query": user_query,


            "document_text": document_text,


            "chat_history": history,


            "clauses": [],


            "retrieved_context": {},


            "risks": [],


            "rewrites": [],


            "final_report": {}


        }



        result = agent_app.invoke(

            initial_state

        )



        final_report = result["final_report"]



        add_message(
            session_id,
            "assistant",
            str(final_report)
        )



        return final_report







    # --------------------------------
    # Text only → Smart Router + Memory
    # --------------------------------


    query = user_query.lower().strip()




    question_keywords = [

        "what",

        "why",

        "how",

        "explain",

        "tell",

        "define",

        "describe",

        "meaning",

        "difference",

        "can",

        "should",

        "is",

        "are"

    ]





    is_question = (

        query.endswith("?")

        or

        any(

            word in query.split()

            for word in question_keywords

        )

    )





    # Add memory context

    memory_query = f"""

Previous conversation:

{history}


Current user request:

{user_query}


"""






    # Legal Q&A RAG

    if is_question:


        response = answer_question(

            memory_query

        )






    # Clause Review RAG

    else:


        response = review_clause(

            memory_query

        )







    # Save AI response


    add_message(

        session_id,

        "assistant",

        str(response)

    )




    return response