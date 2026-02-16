import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.text_chunks = []

    def add(self, embeddings, chunks):
        self.index.add(np.array(embeddings))
        self.text_chunks.extend(chunks)

    def search(self, query_embedding, k=3):
        D, I = self.index.search(np.array(query_embedding), k)
        return [self.text_chunks[i] for i in I[0]]
    
    def get_all_chunks(self):
        return self.text_chunks  # return a list of strings
