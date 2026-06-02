from backend.review.document_review import review_document


contract = """

1. Termination

The company may terminate this agreement at any time without notice.


2. Liability

The vendor shall be responsible for all damages, losses and claims without any limitation of liability.


3. Confidentiality

Both parties agree to protect confidential information.

"""


result = review_document(contract)


print(result)