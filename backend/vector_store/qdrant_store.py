# qdrant_store.py


# json handling
import json


# file paths
from pathlib import Path



# progress bar
from tqdm import tqdm



# qdrant client
from qdrant_client import QdrantClient



# qdrant classes
from qdrant_client.models import (

    Distance,

    VectorParams,

    PointStruct

)



# batch embedding function
from backend.vector_store.embeddings import (

    create_embeddings

)





# chunk file location
CHUNKS_FILE = Path(

    "data/processed/chunks.json"

)



# qdrant collection
COLLECTION_NAME = "legal_knowledge"




# local qdrant database
client = QdrantClient(

    path="qdrant_db"

)





# create collection
def create_collection():


    # check existing collections
    collections = client.get_collections()


    names = [

        collection.name

        for collection in collections.collections

    ]



    # remove old collection
    if COLLECTION_NAME in names:


        client.delete_collection(

            collection_name=COLLECTION_NAME

        )



    # create fresh collection
    client.create_collection(


        collection_name=COLLECTION_NAME,


        vectors_config=VectorParams(


            # BGE base embedding size
            size=768,


            # cosine similarity search
            distance=Distance.COSINE

        )

    )





# load chunks from json
def load_chunks():


    with open(

        CHUNKS_FILE,

        "r",

        encoding="utf-8"

    ) as file:


        chunks = json.load(file)


    return chunks






# create embeddings and save to qdrant
def store_chunks():


    # read chunks
    chunks = load_chunks()



    print(

        f"Loaded {len(chunks)} chunks"

    )



    # number uploaded together
    batch_size = 100



    # loop through chunks
    for start in tqdm(


        range(
            0,
            len(chunks),
            batch_size
        ),


        desc="Uploading batches to Qdrant"

    ):



        # take 100 chunks
        batch = chunks[

            start:start + batch_size

        ]




        # collect text
        texts = [

            item["text"]

            for item in batch

        ]




        # one embedding call for 100 chunks
        vectors = create_embeddings(

            texts

        )




        # qdrant storage objects
        points = []




        for index, item in enumerate(batch):


            point = PointStruct(


                id=start + index,


                vector=vectors[index],


                payload={


                    "text":

                    item["text"],


                    **item["metadata"]

                }

            )



            points.append(

                point

            )




        # insert batch
        client.upsert(


            collection_name=COLLECTION_NAME,


            points=points

        )





# main
if __name__ == "__main__":



    create_collection()



    store_chunks()



    print(

        "Qdrant knowledge base created successfully"

    )