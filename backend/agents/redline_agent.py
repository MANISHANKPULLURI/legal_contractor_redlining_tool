def redline_agent(state):


    enhanced_rewrites = []


    risks = state.get(
        "risks",
        []
    )


    rewrites = state.get(
        "rewrites",
        []
    )



    for rewrite in rewrites:


        matched_risk = None


        for risk in risks:


            if (
                risk.get("clause_number")
                ==
                rewrite.get("clause_number")
            ):

                matched_risk = risk

                break



        analysis = {}


        if matched_risk:


            analysis = matched_risk.get(
                "analysis",
                {}
            )



        enhanced_rewrites.append(
            {

                **rewrite,


                "risk_level":
                analysis.get(
                    "risk_level",
                    "LOW"
                ),


                "issues":
                analysis.get(
                    "issues",
                    []
                ),


                "explanation":
                analysis.get(
                    "explanation",
                    ""
                ),


                "recommendation":
                analysis.get(
                    "recommendation",
                    ""
                )

            }
        )




    state["rewrites"] = enhanced_rewrites



    final_report = {

        "total_clauses": len(
            state["clauses"]
        ),


        "risks":
        state["risks"],


        "suggested_rewrites":
        enhanced_rewrites

    }



    state["final_report"] = final_report


    return state