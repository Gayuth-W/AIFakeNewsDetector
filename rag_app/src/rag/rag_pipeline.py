from rag_app.src.rag.embeddings import embed_query
from rag_app.src.rag.vector_store import similarity_search

def retrieve_context(query: str, k: int = 5) -> str:
    """
    Retrieve relevant context for a user query
    """
    query_embedding = embed_query(query)
    documents = similarity_search(query_embedding, k=k)

    if not documents:
        return ""

    return "\n".join(documents)
