
from qdrant_client import QdrantClient


client = QdrantClient(
    path="qdrant_db"
)


collections = client.get_collections()

print("Collections:")

for c in collections.collections:
    print(c.name)


info = client.get_collection(
    collection_name="legal_knowledge"
)

print(
    "Total vectors:",
    info.points_count
)