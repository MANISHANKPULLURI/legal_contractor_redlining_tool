from backend.review.review_chain import review_clause


import re


def split_into_clauses(document_text):

    parts = re.split(
        r"\n\d+\.\s+",
        document_text
    )


    clauses = []


    for part in parts:

        cleaned = part.strip()


        if len(cleaned) > 40:

            clauses.append(
                cleaned
            )


    return clauses


def review_document(document_text):

    clauses = split_into_clauses(document_text)


    results = []


    for index, clause in enumerate(clauses):

        print(
            f"Reviewing clause {index+1}/{len(clauses)}"
        )


        analysis = review_clause(
            clause
        )


        results.append(
            {
                "clause_number": index + 1,
                "original_clause": clause,
                "analysis": analysis
            }
        )


    return {
        "total_clauses": len(clauses),
        "review": results
    }