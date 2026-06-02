
from backend.review.review_chain import review_clause


clause = """

The vendor shall be responsible for all damages,
losses and claims without any limitation of liability.

"""


answer = review_clause(clause)


print(answer)
