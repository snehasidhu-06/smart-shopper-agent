import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

INDEX_PATH = os.path.join("embeddings", "faiss_index.index")
DATA_PATH = os.path.join("embeddings", "product_data.pkl")

# Load model, index, and data once when this file is imported
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(INDEX_PATH)

with open(DATA_PATH, "rb") as f:
    product_df = pickle.load(f)

def search_products(query, top_k=5):
    # Convert user query into a vector
    query_vector = model.encode([query]).astype("float32")

    # Search FAISS index for closest matches
    distances, indices = index.search(query_vector, top_k)

    # Get matching products
    results = product_df.iloc[indices[0]].copy()
    results["distance"] = distances[0]

    return results.to_dict(orient="records")

if __name__ == "__main__":
    # Quick test
    test_query = "waterproof bluetooth earbuds"
    results = search_products(test_query, top_k=3)

    print(f"\nTop results for: '{test_query}'\n")
    for i, product in enumerate(results, 1):
        print(f"{i}. {product['title']}")
        print(f"   Price: PKR {product['price']} | Rating: {product['rating']}")
        print()