# embeddings.py


# sentence transformer is used for embedding generation
from sentence_transformers import SentenceTransformer



# BGE embedding model
MODEL_NAME = "BAAI/bge-base-en-v1.5"



# load model once
embedding_model = SentenceTransformer(
    MODEL_NAME
)




# used while creating vector database
# converts multiple chunks together
def create_embeddings(texts):


    # BGE retrieval instruction
    formatted_texts = [

        "Represent this legal document for retrieval: " + text

        for text in texts

    ]



    # batch embedding generation
    vectors = embedding_model.encode(


        # list of documents
        formatted_texts,


        # internally process 32 at a time
        batch_size=32,


        # cosine similarity works better
        normalize_embeddings=True,


        # show embedding progress bar
        show_progress_bar=True

    )



    # convert numpy array to list
    return vectors.tolist()






# used later during user query retrieval
# only one question comes, so single embedding
def create_embedding(text):


    # BGE query instruction
    query = (

        "Represent this question for searching legal documents: "
        + text

    )



    vector = embedding_model.encode(

        query,


        normalize_embeddings=True

    )



    return vector.tolist()