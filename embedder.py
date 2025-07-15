# embedder.py
import pickle
from sentence_transformers import SentenceTransformer
from glof_chatbot.app.logic.parser import parse_ontology

def embed_chunks(model_name="all-MiniLM-L6-v2"):
    """
    Parse the ontology, embed the resulting chunks, 
    and save (chunks, embeddings) into data/chunk_embeddings.pkl
    """
    print("🔍 Parsing ontology and generating chunks...")
    chunks = parse_ontology("data/Glacier Lake.ttl")
    print(f"➡️  Parsed {len(chunks)} chunks.")

    print("🧠 Embedding chunks with", model_name)
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks, convert_to_tensor=True)

    out_path = "data/chunk_embeddings.pkl"
    print(f"💾 Saving chunks + embeddings to {out_path}")
    with open(out_path, "wb") as f:
        pickle.dump((chunks, embeddings), f)

    print("✅ Done.")

if __name__ == "__main__":
    embed_chunks()
