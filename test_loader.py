from backend.document_loader.loader import load_document


file_path = "/Users/manishank/Desktop/LegalContractor/sample_contract.pdf"


text = load_document(
    file_path
)


print(text[:1000])