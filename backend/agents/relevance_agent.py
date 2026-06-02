from backend.llm.model import generate_response



def relevance_agent(state):


    clauses = state["clauses"]

    user_query = state["user_query"]


    relevant_clauses = []



    # -------------------------------
    # No query = full review
    # -------------------------------

    if (
        user_query is None
        or user_query.strip() == ""
        or "review" in user_query.lower()
    ):


        print(
            "RELEVANCE: Full review mode"
        )


        return state





    for clause in clauses:


        prompt = f"""

You are a legal contract filtering agent.


USER REQUEST:

{user_query}



CONTRACT CLAUSE:

{clause["text"]}



Decide whether this clause matches
the user's requested review area.


Examples:


User:
Only check liability risks


Clause:
The vendor liability shall...


Answer:
YES



User:
Only check liability risks


Clause:
Termination of agreement...


Answer:
NO



Return ONLY:

YES

or

NO

"""




        result = generate_response(
            prompt
        )





        # Groq/API safety

        if isinstance(result, dict):


            print(
                "Relevance error:",
                result
            )


            continue





        if "YES" in result.upper():


            # IMPORTANT:
            # keep full object
            # keeps original number

            relevant_clauses.append(
                clause
            )







    print(
        "RELEVANT CLAUSES:",
        len(relevant_clauses)
    )






    if len(relevant_clauses) > 0:


        state["clauses"] = relevant_clauses






    return state