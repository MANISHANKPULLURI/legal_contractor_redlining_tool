# import json module to read CUAD json
import json


# import Path to handle file locations
from pathlib import Path



# location of original CUAD file
CUAD_FILE = Path(
    "data/knowledgebase/CUADv1.json"
)


# output after extraction
OUTPUT_FILE = Path(
    "data/processed/extracted_contracts.json"
)



# load CUAD json data
def load_cuad():


    # open CUAD file
    with open(
        CUAD_FILE,
        "r",
        encoding="utf-8"
    ) as file:


        # convert json into python dictionary
        data = json.load(file)


    return data




# extract useful information
def extract_contracts(data):


    # final list of contracts
    contracts = []



    # loop through every contract
    for document in data["data"]:


        # contract filename/title
        contract_name = document["title"]



        # CUAD stores text inside paragraphs
        for paragraph in document["paragraphs"]:



            # actual full contract text
            contract_text = paragraph["context"]



            # list for clause information
            clauses = []



            # qas contains legal clause annotations
            for qa in paragraph["qas"]:



                # skip missing clauses
                if qa["is_impossible"]:

                    continue



                # extract clause name from id
                clause_type = qa["id"].split("__")[-1]



                # store all found answers
                for answer in qa["answers"]:


                    clauses.append(

                        {

                            "clause_type": clause_type,

                            "text": answer["text"]

                        }

                    )



            # store one contract
            contracts.append(

                {

                    "contract_name": contract_name,

                    "text": contract_text,

                    "clauses": clauses,

                    "source": "CUAD"

                }

            )



    return contracts





# save extracted data
def save_contracts(contracts):


    # create processed folder if missing
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    # save json
    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            contracts,
            file,
            indent=2
        )




# program starts here
if __name__ == "__main__":


    # load original data
    data = load_cuad()



    # extract contracts and clauses
    contracts = extract_contracts(data)



    # save processed data
    save_contracts(contracts)



    # print result
    print(
        f"Extracted {len(contracts)} contracts"
    )