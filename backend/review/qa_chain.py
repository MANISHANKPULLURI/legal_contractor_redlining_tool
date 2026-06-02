from backend.retrieval.retrievar import retrieve

from backend.llm.model import generate_response



def answer_question(query):


    docs = retrieve(

        query

    )



    context = "\n\n".join(

        [

            doc["text"]

            for doc in docs[:5]

        ]

    )





    prompt = f"""

You are a legal AI assistant.

Your job is to answer legal questions.

Do NOT analyze the user's question as a contract clause.

Use the provided legal knowledge.

LEGAL KNOWLEDGE:

{context}


USER QUESTION:

{query}


Give a clear helpful explanation.

"""




    response = generate_response(

        prompt

    )



    return response