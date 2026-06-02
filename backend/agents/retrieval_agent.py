from backend.retrieval.retrievar import retrieve
from backend.retrieval.reranker import rerank



def retrieval_agent(state):


    clauses = state["clauses"]

    user_query = state["user_query"]


    retrieved_context = {}




    for clause in clauses:


        clause_number = clause["number"]

        clause_text = clause["text"]




        retrieval_query = f"""

User review goal:

{user_query}


Contract clause:

{clause_text}

"""




        docs = retrieve(
            retrieval_query,
            top_k=20
        )





        best_docs = rerank(

            retrieval_query,

            docs,

            top_k=5

        )






        retrieved_context[
            clause_number
        ] = best_docs







    state["retrieved_context"] = retrieved_context



    return state