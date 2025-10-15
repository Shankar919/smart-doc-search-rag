import os
from typing import List
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

def embed_texts_openai(texts: List[str]):
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    resp = openai.Embedding.create(model='text-embedding-3-small', input=texts)
    return [r['embedding'] for r in resp['data']]

def embed_texts_local(texts: List[str], model_name: str = 'all-MiniLM-L6-v2'):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    embs = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embs.tolist()

def embed_texts(texts):
    if OPENAI_KEY:
        return embed_texts_openai(texts)
    return embed_texts_local(texts, os.getenv('EMB_MODEL','all-MiniLM-L6-v2'))
