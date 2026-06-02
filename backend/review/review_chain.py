import json
import re

from backend.retrieval.retrievar import retrieve
from backend.retrieval.reranker import rerank

from backend.llm.prompts import LEGAL_REVIEW_PROMPT
from backend.llm.model import generate_response



def review_clause(clause):

    # step 1 retrieval
    docs = retrieve(
        clause,
        top_k=20
    )


    # step 2 reranking
    best_docs = rerank(
        clause,
        docs,
        top_k=5
    )


    context = "\n\n".join(
        [
            d["text"]
            for d in best_docs
        ]
    )


    # step 3 prompt
    prompt = LEGAL_REVIEW_PROMPT.format(
        clause=clause,
        context=context
    )


    # step 4 LLM reasoning
    result = generate_response(prompt)


    # step 5 convert LLM string -> JSON object
    try:
        cleaned = re.sub(
            r"```json|```",
            "",
            result
        ).strip()


        return json.loads(cleaned)


    except Exception:

        return {
            "error": "JSON parsing failed",
            "raw": result
        }