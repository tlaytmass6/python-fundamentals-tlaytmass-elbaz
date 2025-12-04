import os
from dotenv import load_dotenv
import openai
import pandas as pd
import glob
import numpy as np
import pickle

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("API key not found. Check your .env file.")

phrases = [
    "Biomedical engineering combines medicine and engineering to improve healthcare",
    "Medical imaging techniques are essential in BME research",
    "BME innovations help develop prosthetics and medical devices"
]

embeddings = []
for p in phrases:
    response = openai.Embedding.create(
        input=p,
        model="text-embedding-3-small"
    )
    embeddings.append(response['data'][0]['embedding'])

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

print("\nCosine similarities between BME phrases:")
for i in range(len(phrases)):
    for j in range(i+1, len(phrases)):
        sim = cosine_similarity(embeddings[i], embeddings[j])
        print(f"'{phrases[i]}' <-> '{phrases[j]}': {sim:.4f}")

files = glob.glob("articles/*.txt")  
df = pd.DataFrame({"filename": files})
df["text"] = df["filename"].apply(lambda x: open(x, "r").read())

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

df["chunks"] = df["text"].apply(chunk_text)
all_chunks = [chunk for chunks in df["chunks"] for chunk in chunks]
print(f"\nTotal chunks created: {len(all_chunks)}")

chunk_embeddings = []
for i, chunk in enumerate(all_chunks, 1):
    response = openai.Embedding.create(
        input=chunk,
        model="text-embedding-3-small"
    )
    chunk_embeddings.append(response['data'][0]['embedding'])
    if i % 10 == 0 or i == len(all_chunks):
        print(f"Processed {i}/{len(all_chunks)} chunks...")

with open("embeddings.pkl", "wb") as f:
    pickle.dump({"chunks": all_chunks, "embeddings": chunk_embeddings}, f)

print("\nAll embeddings saved to 'embeddings.pkl'")
