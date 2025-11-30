from sentence_transformers import SentenceTransformer


def load_embedder(model_name):
print("Loading embedding model...")
model = SentenceTransformer(model_name)
print("Embedding model loaded.")
return model


def embed_texts(model, texts):
return model.encode(texts, show_progress_bar=False).tolist()

