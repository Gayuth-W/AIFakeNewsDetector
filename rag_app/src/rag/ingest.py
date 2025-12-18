import uuid
from .embeddings import embed_texts
from .vector_store import add_documents

def ingest_texts(texts: list[str]):
    embeddings = embed_texts(texts)
    ids = [str(uuid.uuid4()) for _ in texts]

    add_documents(
        ids=ids,
        texts=texts,
        embeddings=embeddings
    )

if __name__ == "__main__":
    sample_docs = [
        "The World Health Organization has stated that vaccines do not cause autism.",
        "Climate change is primarily driven by human activities such as burning fossil fuels.",
        "There is no scientific evidence supporting the claim that 5G spreads COVID-19."
    ]

    ingest_texts(sample_docs)
    print("✅ Sample knowledge ingested")
