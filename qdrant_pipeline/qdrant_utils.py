from qdrant_client import QdrantClient
client.recreate_collection(
collection_name=name,
vectors_config=rest.VectorParams(
size=vector_size,
distance=rest.Distance.COSINE
)
)
else:
print(f"Collection '{name}' already exists.")


def find_existing(client, collection_name, ids):
found = set()
for i in range(0, len(ids), 200):
batch = ids[i:i+200]
items = client.retrieve(collection_name=collection_name, ids=batch)
for p in items:
found.add(p.id)
return found


def upsert_points(client, collection_name, rows):
"""
rows: list of { point_id, vector, payload }
"""
payloads = []
for r in rows:
payloads.append(
rest.PointStruct(
id=r["point_id"],
vector=r["vector"],
payload=r["payload"]
)
)

client.upsert(collection_name=collection_name, points=payloads)
print(f"Inserted {len(rows)} new points.")


def search_qdrant(client, collection_name, vector, limit=5):
results = client.search(
collection_name=collection_name,
query_vector=vector,
limit=limit
)
return results
