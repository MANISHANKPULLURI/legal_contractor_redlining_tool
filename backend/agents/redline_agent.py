def redline_agent(state):

    final_report = {
        "total_clauses": len(
            state["clauses"]
        ),

        "risks": state["risks"],

        "suggested_rewrites": state["rewrites"]
    }


    state["final_report"] = final_report


    return state