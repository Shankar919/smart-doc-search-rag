import os
from qdrant_client import QdrantClient
from qdrant_client.http import models

Q_HOST = os.getenv('QDRANT_HOST', 'http://localhost')
Q_PORT = int(os.getenv('QDRANT_PORT', 6333))
COLLECTION = os.getenv('QDRANT_COLLECTION', 'kb')

# QdrantClient accepts url without port sometimes; allow either
URL = f"{Q_HOST}:{Q_PORT}" if 'http' in Q_HOST and ':' not in Q_HOST else f"{Q_HOST}:{Q_PORT}"
client = QdrantClient(url=URL, api_key=os.getenv('QDRANT_API_KEY') or None)

def create_collection(dim: int):
    try:
        client.recreate_collection(
            collection_name=COLLECTION,
            vectors_config=models.VectorParams(size=dim, distance=models.Distance.COSINE),
        )
    except Exception as e:
        # recreate_collection may fail if already exists with same params; try create
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=models.VectorParams(size=dim, distance=models.Distance.COSINE),
        )

def upsert_vectors(ids, vectors, metadatas):
    batch = models.Batch(
        ids=ids,
        vectors=vectors,
        payloads=metadatas
    )
    client.upsert(collection_name=COLLECTION, batch=batch)

def search_vector(query_vector, top_k=5):
    hits = client.search(collection_name=COLLECTION, query_vector=query_vector, limit=top_k)
    # Return simplified hits
    return hits
