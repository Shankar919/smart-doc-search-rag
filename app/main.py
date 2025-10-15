import os, tempfile
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from .vectorize import index_file
from .qdrant_client import search_vector
from .embeddings import embed_texts
from .synth import synthesize_answer
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post('/ingest')
async def ingest(file: UploadFile = File(...)):
    ext = file.filename.split('.')[-1].lower()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.'+ext)
    tmp.write(await file.read())
    tmp.close()
    count = index_file(tmp.name, file.filename)
    return {'status':'ok','chunks_indexed':count}

@app.post('/query')
async def query(req: QueryRequest):
    qvecs = embed_texts([req.query])
    qvec = qvecs[0]
    hits = search_vector(qvec, top_k=req.top_k)
    # format hits
    snippets = []
    for h in hits:
        # qdrant returns objects with id, payload, score
        snippets.append({'id': getattr(h,'id', None) or h.id, 'score': getattr(h,'score', None) or h.score, 'payload': getattr(h,'payload', None) or h.payload})
    answer = synthesize_answer(req.query, snippets)
    return {'answer': answer, 'sources': snippets}
