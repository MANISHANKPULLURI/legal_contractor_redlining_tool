from backend.review.document_review import split_into_clauses



def parser_agent(state):


    document_text = state["document_text"]


    raw_clauses = split_into_clauses(
        document_text
    )



    print(
        "CLAUSES FOUND:",
        len(raw_clauses)
    )



    # Preserve original clause number
    # even after relevance filtering

    clauses = []


    for index, clause in enumerate(
        raw_clauses
    ):


        clauses.append(
            {
                "number": index + 1,

                "text": clause
            }
        )




    state["clauses"] = clauses



    return state