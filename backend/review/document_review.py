# backend/review/document_review.py

import re





def split_into_clauses(document_text):


    """
    General legal contract splitter.

    Supports:
    - Section 1
    - Section 1.1
    - ARTICLE I
    - 1. Clause Title
    - 1.1 Clause Title
    - 1) Clause Title
    - CLAUSE 1
    """



    text = document_text.strip()



    # normalize line breaks

    text = re.sub(
        r"\n+",
        "\n",
        text
    )






    parts = re.split(

        r"""
        (?=
            (?:Section\s+\d+(?:\.\d+)?)
            |
            (?:ARTICLE\s+[IVXLC]+)
            |
            (?:CLAUSE\s+\d+)
            |
            (?:^\d+(?:\.\d+)?[\.\)]\s+)
        )
        """,


        text,


        flags=
        re.IGNORECASE
        |
        re.MULTILINE
        |
        re.VERBOSE

    )








    clauses = []



    for part in parts:


        cleaned = part.strip()



        if len(cleaned) > 80:


            clauses.append(
                cleaned
            )









    # fallback for unusual contracts

    if len(clauses) <= 1:


        parts = re.split(

            r"\n(?=[A-Z][A-Z\s]{5,}:?)",

            text

        )



        clauses = [

            p.strip()

            for p in parts

            if len(
                p.strip()
            ) > 80

        ]







    # final fallback

    if len(clauses) <= 1:


        clauses = [

            text

        ]





    return clauses