# reranker.py


# import BGE reranker
from FlagEmbedding import FlagReranker



# load reranker once
reranker_model = FlagReranker(

    "BAAI/bge-reranker-base",

    use_fp16=True

)





# rerank retrieved documents
def rerank(

    query,

    documents,

    top_k=5

):


    # create query-document pairs
    pairs = [

        [

            query,

            document["text"]

        ]

        for document in documents

    ]




    # calculate relevance scores
    scores = reranker_model.compute_score(

        pairs

    )




    # attach scores with documents
    ranked_documents = []


    for document, score in zip(

        documents,

        scores

    ):


        document["rerank_score"] = score


        ranked_documents.append(

            document

        )




    # sort by reranker score
    ranked_documents.sort(

        key=lambda x: x["rerank_score"],

        reverse=True

    )




    # return best documents
    return ranked_documents[:top_k]





# testing
if __name__ == "__main__":


    from backend.retrieval.retrievar import retrieve



    query = (

        "What is a risky termination clause?"

    )



    # first retrieve from qdrant
    results = retrieve(

        query,

        top_k=8

    )



    # rerank
    final_results = rerank(

        query,

        results,

        top_k=3

    )




    for doc in final_results:


        print(

            "\nRerank Score:",

            doc["rerank_score"]

        )


        print(

            doc["text"][:500]

        )
