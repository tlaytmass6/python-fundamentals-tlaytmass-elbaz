
import os
import pandas as pd
import re
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from sentence_transformers import SentenceTransformer



COLLECTION_NAME = "project_chunks"

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

VECTOR_SIZE = 384

CSV_FILE = "articles.csv"   



def connect_qdrant():
    client = QdrantClient(
        host="localhost",
        port=6333
    )
    return client



def create_collection(client):
    """Creates the collection if it doesn't already exist."""
    collections = client.get_collections().collections
    existing_names = [c.name for c in collections]

    if COLLECTION_NAME not in existing_names:
        print(f"Creating new collection: {COLLECTION_NAME}")
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=rest.VectorParams(
                size=VECTOR_SIZE,
                distance=rest.Distance.COSINE
            )
        )
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")



def chunk_text(text, max_chars=1000, overlap=200):
    text = re.sub(r"\s+", " ", text).strip()

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + max_chars, len(text))
        chunk = text[start:end].strip()
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0

    return chunks


def load_articles():
    print(f"Loading {CSV_FILE} ...")
    df = pd.read_csv(CSV_FILE)
    print(f"Loaded {len(df)} articles.")
    return df



def make_chunk_dataframe(articles_df):
    all_rows = []

    for _, row in articles_df.iterrows():
        article_id = str(row["id"])
        text = str(row["content"])
        chunks = chunk_text(text)

        for idx, chunk in enumerate(chunks):
            all_rows.append({
                "point_id": f"{article_id}::{idx}",  
                "article_id": article_id,
                "chunk_index": idx,
                "text": chunk,
                "title": row.get("title", None),
                "source": row.get("source", None)
            })

    chunks_df = pd.DataFrame(all_rows)
    print(f"Created {len(chunks_df)} text chunks.")
    return chunks_df



def load_embedding_model():
    print("Loading embedding model... (this might take 5–10 seconds)")
    model = SentenceTransformer(EMBED_MODEL_NAME)
    print("Embedding model ready.")
    return model


def embed_texts(model, text_list: List[str]):
    return model.encode(text_list, show_progress_bar=False).tolist()



def find_existing_points(client, point_ids):
    existing = set()

    for i in range(0, len(point_ids), 200):
        batch = point_ids[i:i+200]
        results = client.retrieve(collection_name=COLLECTION_NAME, ids=batch)

        for point in results:
            existing.add(point.id)

    print(f"{len(existing)} existing points found in Qdrant.")
    return existing



def upsert_points(client, rows):

    qdrant_points = []
    for r in rows:
        qdrant_points.append(
            rest.PointStruct(
                id=r["point_id"],
                vector=r["vector"],
                payload={
                    "article_id": r["article_id"],
                    "chunk_index": r["chunk_index"],
                    "text": r["text"][:300],   
                    "title": r["title"],
                    "source": r["source"]
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=qdrant_points
    )

    print(f"Uploaded {len(rows)} new chunks to Qdrant.")


def search_query(client, model, user_query, top_k=5):
    query_vec = embed_texts(model, [user_query])[0]

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vec,
        limit=top_k
    )

    print("\nSearch Results:")
    for r in results:
        print("-" * 40)
        print("Score:", r.score)
        print("Title:", r.payload.get("title"))
        print("Source:", r.payload.get("source"))
        print("Preview:", r.payload.get("text"))
    print("-" * 40)



def main():
    client = connect_qdrant()
    create_collection(client)
    df = load_articles()
    chunks_df = make_chunk_dataframe(df)

    point_ids = list(chunks_df["point_id"])

    existing_points = find_existing_points(client, point_ids)

    model = load_embedding_model()

    rows_to_upload = []
    for _, row in chunks_df.iterrows():
        pid = row["point_id"]
        if pid in existing_points:
            continue  

        vec = embed_texts(model, [row["text"]])[0] 

        rows_to_upload.append({
            "point_id": pid,
            "vector": vec,
            "article_id": row["article_id"],
            "chunk_index": row["chunk_index"],
            "text": row["text"],
            "title": row["title"],
            "source": row["source"]
        })

    print(f"{len(rows_to_upload)} new chunks need uploading.")

    if rows_to_upload:
        upsert_points(client, rows_to_upload)
    else:
        print("No new chunks to upload.")

    print("\nTry a demo search:")
    search_query(client, model, "how to set up qdrant", top_k=5)



if __name__ == "__main__":
    main()
