# backend/review/document_review.py

import re


def split_into_clauses(document_text):
    """
    Split contracts into real legal sections instead of random chunks.
    Supports:
    Section 1
    Section 1.1
    ARTICLE I
    numbered clauses
    """

    text = document_text.strip()

    # normalize spaces
    text = re.sub(r"\n+", "\n", text)

    # split before legal section headings
    parts = re.split(
        r"""
        (?=
            (?:Section\s+\d+(?:\.\d+)?)
            |
            (?:ARTICLE\s+[IVXLC]+)
            |
            (?:^\d+\.\d+\s+)
        )
        """,
        text,
        flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
    )

    clauses = []

    for part in parts:
        cleaned = part.strip()

        # remove tiny useless chunks
        if len(cleaned) > 100:
            clauses.append(cleaned)

    # fallback if regex fails
    if len(clauses) <= 1:
        paragraphs = text.split("\n\n")

        clauses = [p.strip() for p in paragraphs if len(p.strip()) > 100]

    return clauses
