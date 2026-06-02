from backend.document_loader.loader import load_document
from backend.router.query_router import handle_request


# step 1: load uploaded document

document_text = load_document(
    "sample_contract.pdf"
)


# step 2: send extracted text to router

result = handle_request(

    user_query="Review this contract",

    document_text=document_text

)


print(result)