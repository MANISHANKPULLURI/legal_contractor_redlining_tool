# chunker.py


# used to read and write json files
import json


# used for safe file path handling
from pathlib import Path


# unique id generation for chunks
import uuid



# extracted contracts from extract_cuad.py
INPUT_FILE = Path(
    "data/processed/extracted_contracts.json"
)



# final chunk output
OUTPUT_FILE = Path(
    "data/processed/chunks.json"
)



# maximum characters in one chunk
CHUNK_SIZE = 1200



# repeated characters between chunks
CHUNK_OVERLAP = 200





# load extracted CUAD contracts
def load_contracts():


    # open processed contract file
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:


        # convert json into python list
        contracts = json.load(file)


    return contracts





# split large legal document into overlapping chunks
def split_text(
    text
):


    # stores document pieces
    chunks = []



    # first character index
    start = 0



    # continue until complete text processed
    while start < len(text):


        # ending position
        end = start + CHUNK_SIZE



        # extract text window
        chunk = text[
            start:end
        ]



        # avoid empty chunks
        if chunk.strip():


            chunks.append(
                chunk
            )



        # move forward but keep overlap
        start = end - CHUNK_OVERLAP



    return chunks





# extract clause labels from CUAD annotations
def get_clause_types(
    contract
):


    # collect clause names
    clause_types = [

        clause["clause_type"]

        for clause in contract.get(
            "clauses",
            []
        )

    ]



    # remove duplicate clause names
    return list(
        set(
            clause_types
        )
    )





# convert contracts into vector ready chunks
def create_chunks(
    contracts
):


    # final output list
    all_chunks = []



    # process each contract
    for contract in contracts:



        # get clause categories
        clause_types = get_clause_types(
            contract
        )



        # split full contract
        text_chunks = split_text(
            contract["text"]
        )



        # process each chunk
        for index, chunk_text in enumerate(text_chunks):


            # create chunk object
            chunk = {


                # globally unique chunk id
                "chunk_id":
                str(
                    uuid.uuid4()
                ),



                # chunk number inside contract
                "chunk_index":
                index,



                # text that becomes embedding
                "text":
                chunk_text,



                # information stored with vector
                "metadata": {


                    # original document name
                    "contract_name":
                    contract["contract_name"],



                    # dataset name
                    "source":
                    contract["source"],



                    # legal categories available
                    "clause_types":
                    clause_types,



                    # chunk size information
                    "chunk_size":
                    len(
                        chunk_text
                    )

                }

            }



            # store chunk
            all_chunks.append(
                chunk
            )



    return all_chunks





# save chunks json
def save_chunks(
    chunks
):


    # create folder automatically
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )



    # save json file
    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            chunks,
            file,
            indent=2,
            ensure_ascii=False
        )





# script execution starts here
if __name__ == "__main__":


    # load contracts
    contracts = load_contracts()



    # create chunks
    chunks = create_chunks(
        contracts
    )



    # save chunks
    save_chunks(
        chunks
    )



    # final status
    print(
        f"Created {len(chunks)} chunks"
    )