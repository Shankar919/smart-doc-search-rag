import os, uuid
from .utils import extract_text_from_pdf, clean_text, chunk_text
from .qdrant_client import create_collection, upsert_vectors
from .embeddings import embed_texts
from dotenv import load_dotenv

load_dotenv()
EMB_DIM = int(os.getenv('EMB_DIM', 384))

def index_file(path, source_name):
    text = extract_text_from_pdf(path)
    text = clean_text(text)
    chunks = chunk_text(text)
    ids = []
    vectors = []
    metas = []
    # Batch embeddings for efficiency
    texts = chunks
    embeddings = embed_texts(texts)
    for i, (chunk, vec) in enumerate(zip(chunks, embeddings)):
        _id = str(uuid.uuid4())
        ids.append(_id)
        vectors.append(vec)
        metas.append({'source': source_name, 'chunk_id': i, 'text': chunk[:500]})
    create_collection(EMB_DIM)
    upsert_vectors(ids, vectors, metas)
    return len(ids)
