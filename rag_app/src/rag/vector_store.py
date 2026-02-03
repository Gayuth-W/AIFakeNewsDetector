import chromadb
from chromadb.config import Settings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)


client = chromadb.Client(
    Settings(
        persist_directory=str(CHROMA_DIR),
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(name="fake_news_knowledge")

def add_documents(ids, texts, embeddings):
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings
    )
    # ✅ No persist() in new Chroma versions

def similarity_search(query_embedding, k=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    return results["documents"][0]
