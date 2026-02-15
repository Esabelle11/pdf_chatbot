from .embedding import embed_texts

def retrieve(store, query, k=3):
    query_embedding = embed_texts([query])
    return store.search(query_embedding, k)
