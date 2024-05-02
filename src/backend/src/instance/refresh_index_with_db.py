import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import sqlite3

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
faiss_index = faiss.IndexFlatL2(384) # Note the size of the vector because of this specific model
faiss_index = faiss.IndexIDMap(faiss_index)
con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute("SELECT * FROM notes")

for row in cur:
    emb = model.encode(row[(len(row)-1)])
    faiss_index.add_with_ids(np.array([emb]), np.array([row[0]]))

cur.execute("SELECT * FROM links")

for row in cur:
    emb = model.encode(row[(len(row)-1)])
    faiss_index.add_with_ids(np.array([emb]), np.array([row[0]]))

cur.execute("SELECT * FROM screenshots")

for row in cur:
    emb = model.encode(row[(len(row)-1)])
    faiss_index.add_with_ids(np.array([emb]), np.array([row[0]]))

faiss.write_index(faiss_index, "/Users/ryuparish/Code/memosearch/src/backend/src/instance/faiss.index")
