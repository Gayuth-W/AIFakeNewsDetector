import chromadb
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(name="fake_news_knowledge")


def add_documents(ids, texts, embeddings):
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
    )


def similarity_search(query_embedding, k=3):
    count = collection.count()
    if count == 0:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(k, count),
    )
    docs = results["documents"][0]
    return docs if docs else []
