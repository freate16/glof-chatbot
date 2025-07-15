# retriever.py
import torch
import pickle
from sentence_transformers import SentenceTransformer, util

def get_top_chunks(query, top_k=5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    with open("chunk_embeddings.pkl", "rb") as f:
        chunks, embeddings = pickle.load(f)
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    top_results = torch.topk(scores, k=top_k)
    top_chunks = [chunks[idx] for idx in top_results[1]]
    return top_chunks
