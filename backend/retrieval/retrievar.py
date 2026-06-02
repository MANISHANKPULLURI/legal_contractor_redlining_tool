# retriever.py


# qdrant client
from qdrant_client import QdrantClient



# embedding function for query
from backend.vector_store.embeddings import (

    create_embedding

)




# collection name
COLLECTION_NAME = "legal_knowledge"




# connect existing qdrant database
client = QdrantClient(

    path="qdrant_db"

)





# search legal knowledge
def retrieve(

    query,

    top_k=20

):


    # convert question into vector
    query_vector = create_embedding(

        query

    )



    # search qdrant
    results = client.search(


        collection_name=COLLECTION_NAME,


        query_vector=query_vector,


        limit=top_k

    )



    # format output
    documents = []



    for result in results:


        documents.append(

            {

                "score":

                result.score,


                "text":

                result.payload["text"],


                "metadata":

                {

                    key:value

                    for key,value in result.payload.items()

                    if key != "text"

                }

            }

        )



    return documents






# testing retrieval
if __name__ == "__main__":


    query = (

        "What is a risky termination clause?"

    )



    docs = retrieve(

        query

    )



    for doc in docs[:5]:


        print(

            "\nScore:",

            doc["score"]

        )


        print(

            doc["text"][:500]

        )