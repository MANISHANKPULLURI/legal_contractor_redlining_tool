from backend.document_loader.loader import load_document
from backend.router.query_router import handle_request

from backend.redline.generator import create_redline_doc



# Step 1: Load contract

document_text = load_document(
    "sample_contract.pdf"
)



# Step 2: Run Agentic RAG review

result = handle_request(
    user_query="Review this contract",
    document_text=document_text
)



# Step 3: Generate redline DOCX

file_path = create_redline_doc(
    result["suggested_rewrites"]
)



print(
    "Redline document created:",
    file_path
)