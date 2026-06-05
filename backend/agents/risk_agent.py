from backend.review.review_chain import review_clause



def normalize_analysis(item):

    return {

        "risk_level": item.get(
            "risk_level",
            "LOW"
        ),

        "issues": item.get(
            "issues",
            [
                {
                    "issue": item.get(
                        "issue",
                        ""
                    ),

                    "why_risky": item.get(
                        "explanation",
                        ""
                    )
                }
            ]
        ),

        "explanation": item.get(
            "explanation",
            ""
        ),

        "recommendation": item.get(
            "recommendation",
            ""
        ),

        "rewritten_clause": item.get(
            "rewritten_clause",
            ""
        )

    }






def risk_agent(state):


    clauses = state["clauses"]

    user_query = state["user_query"]


    chat_history = state.get(
        "chat_history",
        []
    )


    risks = []


    batch_size = 5





    for start in range(
        0,
        len(clauses),
        batch_size
    ):


        batch = clauses[
            start:start + batch_size
        ]


        formatted_clauses = ""



        for clause in batch:


            formatted_clauses += f"""

CLAUSE NUMBER: {clause["number"]}

{clause["text"]}

"""






        agent_instruction = f"""

You are an expert contract attorney and risk analysis agent.


PREVIOUS CONVERSATION:

{chat_history}


CURRENT USER REVIEW INSTRUCTION:

{user_query}


Analyze the following contract clauses.



RULES:


1. Follow the latest user instruction.


2. Use previous conversation context.


3. If the user asks for a specific risk type
(example: liability, termination, confidentiality),
only analyze that area.


4. For a general contract review:

Analyze EVERY clause provided.

You MUST return exactly ONE JSON object
for EACH clause.

Never skip clauses.

If a clause has no major problem,
mark it LOW risk and explain why.



Return every object with:

- clause_number
- risk_level
- issues
- explanation
- recommendation
- rewritten_clause


The clause_number MUST match the given
CLAUSE NUMBER.



REWRITE RULES:


Do NOT repeat original text.

Fix the actual weakness.



Termination:
- add notice requirement
- fair termination process
- cure period if needed


Liability:
- add liability limitation
- remove unlimited exposure


Confidentiality:
- add definition
- add protection duties
- restrict unauthorized disclosure



Never invent:

- money amounts
- exact days
- percentages
- jurisdiction


Use placeholders:

[X days]

[agreed liability cap]

[agreed time period]

[applicable jurisdiction]



CONTRACT CLAUSES:


{formatted_clauses}


Return ONLY valid JSON list.

"""




        batch_analysis = review_clause(
            agent_instruction
        )






        # --------------------
        # Groq errors
        # --------------------

        if (
            isinstance(batch_analysis, dict)
            and "error" in batch_analysis
        ):


            risks.append(
                {

                    "clause_number":
                    batch[0]["number"],


                    "clause":
                    batch[0]["text"],


                    "analysis": {

                        "risk_level":
                        "ERROR",


                        "issues":[
                            {
                                "issue":
                                "LLM unavailable",

                                "why_risky":
                                batch_analysis["error"]
                            }
                        ],


                        "explanation":
                        batch_analysis["error"],


                        "recommendation":
                        "Try again later",


                        "rewritten_clause":
                        ""

                    }

                }
            )


            continue







    

        if isinstance(
            batch_analysis,
            list
        ):


            for idx, clause in enumerate(batch):


                if idx < len(batch_analysis):


                    analysis = batch_analysis[idx]


                else:


                    # LLM skipped safe clause
                    # create fallback

                    analysis = {

                        "risk_level":
                        "LOW",


                        "issues":
                        [],


                        "explanation":
                        "No major legal risk identified.",


                        "recommendation":
                        "No changes required.",


                        "rewritten_clause":
                        clause["text"]

                    }






                risks.append(
                    {

                        "clause_number":
                        clause["number"],


                        "clause":
                        clause["text"],


                        "analysis":
                        normalize_analysis(
                            analysis
                        )

                    }
                )







        else:


            risks.append(
                {

                    "clause_number":
                    batch[0]["number"],


                    "clause":
                    batch[0]["text"],


                    "analysis":
                    normalize_analysis(
                        batch_analysis
                    )

                }
            )





    state["risks"] = risks


    return state