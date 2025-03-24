from sentence_transformers import SentenceTransformer
import numpy as np


def get_embedding(query):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embedding = model.encode(query)
    return embedding


def get_embedding_array(query):
    embed = get_embedding(query)
    vector_array = np.array(embed, dtype=np.float32)
    return vector_array.tolist()
