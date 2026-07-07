import sqlite3
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
import pickle

DB_PATH = os.path.join("database", "shopper.db")
INDEX_PATH = os.path.join("embeddings", "faiss_index.index")
DATA_PATH = os.path.join("embeddings", "product_data.pkl")

def load_products():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df

def generate_embeddings(df):
    print("Loading embedding model... (this may take a minute the first time)")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Generating embeddings for product titles...")
    search_text = (df["title"].fillna("") + " " + df["category"].fillna("") + " " + df["brand"].fillna("")).tolist()
    embeddings = model.encode(search_text, show_progress_bar=True)

    return np.array(embeddings).astype("float32")

def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

if __name__ == "__main__":
    df = load_products()
    print(f"Loaded {len(df)} products from database.")

    embeddings = generate_embeddings(df)

    index = build_faiss_index(embeddings)
    faiss.write_index(index, INDEX_PATH)
    print(f"FAISS index saved to {INDEX_PATH}")

    with open(DATA_PATH, "wb") as f:
        pickle.dump(df, f)
    print(f"Product data saved to {DATA_PATH}")

    print("Embedding generation complete!")