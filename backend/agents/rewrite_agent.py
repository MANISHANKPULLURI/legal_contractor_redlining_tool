def rewrite_agent(state):


    risks = state["risks"]


    rewrites = []



    for item in risks:


        analysis = item.get(
            "analysis",
            {}
        )


        rewritten_clause = analysis.get(
            "rewritten_clause",
            ""
        )



        rewrites.append(
            {
                "clause_number":
                item.get("clause_number"),


                "original_clause":
                item.get(
                    "clause",
                    ""
                ),


                "rewritten_clause":
                rewritten_clause
            }
        )




    state["rewrites"] = rewrites



    return state