from backend.llm.model import generate_response




def relevance_agent(state):


    clauses = state["clauses"]



    raw_query = state.get(
        "user_query",
        ""
    )



    if raw_query is None:

        raw_query = ""



    user_query = (
        raw_query
        .lower()
        .strip()
    )






    # --------------------------------
    # No specific instruction
    # Full contract review
    # --------------------------------


    if (
        user_query == ""
        or user_query in [
            "review",
            "review contract",
            "analyze",
            "analyze contract",
            "review all",
            "full review"
        ]
    ):


        print(
            "RELEVANCE: Full review mode"
        )


        return state







    # --------------------------------
    # Semantic relevance filtering
    # --------------------------------


    relevant_clauses = []





    for clause in clauses:



        prompt = f"""

You are Lexo's contract relevance agent.



Your task:

Decide whether this contract clause should be selected
for the user's requested review.



You are NOT the risk analyzer.

Only decide relevance.



Rules:

1. Understand legal meaning.

2. Do not depend on exact keyword matching.

3. Match the MAIN purpose/topic of the clause.

4. Do not include a clause only because
   it is generally risky.

5. Select YES only if a legal expert reviewing
   the user's requested area would choose this clause.

6. Ignore unrelated risks because another agent
   will analyze them later.







Examples:


User request:
Review unclear or vague clauses


Clause:
"The provider shall perform services as required
from time to time."


Answer:
YES






User request:
Review unclear or vague clauses


Clause:
"The company may terminate this agreement
without notice."


Answer:
NO


Reason:
The primary issue is termination rights,
not vague wording.







User request:
Review financial exposure


Clause:
"The vendor shall be responsible for all damages."


Answer:
YES








USER REQUEST:

{raw_query}








CONTRACT CLAUSE:

{clause["text"]}








Return ONLY:

YES

or

NO


"""





        result = generate_response(
            prompt
        )






        # LLM/API safety

        if not isinstance(
            result,
            str
        ):


            continue







        answer = (
            result
            .strip()
            .upper()
        )






        if answer.startswith(
            "YES"
        ):


            relevant_clauses.append(
                clause
            )








    print(
        "RELEVANT CLAUSES:",
        len(
            relevant_clauses
        )
    )






    state["clauses"] = relevant_clauses





    return state