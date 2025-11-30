import pandas as pd
def main():

client = connect_qdrant(QDRANT_SERVER_HOST, QDRANT_SERVER_PORT)

create_collection_if_needed(client, COLLECTION_NAME, VECTOR_SIZE)

print(f"Loading {CSV_FILE}...")
df = pd.read_csv(CSV_FILE)

rows = []
for _, row in df.iterrows():
aid = str(row["id"])
parts = chunk_text(row["content"])
for i, text in enumerate(parts):
rows.append({
"point_id": make_id(aid, i),
"article_id": aid,
"chunk_index": i,
"text": text,
"title": row.get("title", None),
"source": row.get("source", None),
})

print(f"Created {len(rows)} chunks.")

ids = [r["point_id"] for r in rows]
existing = find_existing(client, COLLECTION_NAME, ids)
print(f"{len(existing)} points already in Qdrant.")

model = load_embedder(EMBEDDING_MODEL)

new_points = []
for r in rows:
if r["point_id"] in existing:
continue

vec = embed_texts(model, [r["text"]])[0]

info = {
"point_id": r["point_id"],
"vector": vec,
"payload": {
"article_id": r["article_id"],
"chunk_index": r["chunk_index"],
"title": r["title"],
"source": r["source"],
"preview": r["text"][:250],
}
}

new_points.append(info)

if new_points:
upsert_points(client, COLLECTION_NAME, new_points)
else:
print("Nothing new to upload.")

query = "how do I connect qdrant" 
vec = embed_texts(model, [query])[0]

results = search_qdrant(client, COLLECTION_NAME, vec, limit=5)

print("\nSearch Results:\n")
for r in results:
print("------------------------------------")
print("Score:", r.score)
print("Title:", r.payload.get("title"))
print("Source:", r.payload.get("source"))
print("Preview:", r.payload.get("preview"))


if __name__ == "__main__":
main()
