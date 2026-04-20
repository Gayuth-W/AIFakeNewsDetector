import uuid
from pathlib import Path

from .embeddings import embed_texts
from .vector_store import add_documents

DATA_DIR = Path(__file__).parent.parent.parent / "data"
FACT_CHECKS_FILE = DATA_DIR / "fact_checks.txt"

DEFAULT_FACTS = [
    "The World Health Organization has stated that vaccines do not cause autism.",
    "Climate change is primarily driven by human activities such as burning fossil fuels.",
    "There is no scientific evidence supporting the claim that 5G spreads COVID-19.",
    "Drinking bleach does not cure COVID-19 and is extremely dangerous.",
    "The Earth is approximately 4.5 billion years old, supported by radiometric dating.",
    "Human activity is the primary driver of recent global temperature increases.",
    "Face masks help reduce the spread of respiratory viruses including COVID-19.",
    "The moon landing in 1969 was real and has been independently verified by multiple sources.",
    "Flu vaccines cannot give you the flu; they contain inactivated or weakened virus particles.",
    "Chemtrails are a conspiracy theory; contrails are normal water vapor from aircraft engines.",
]


def load_fact_checks() -> list[str]:
    if FACT_CHECKS_FILE.exists():
        facts = [
            line.strip()
            for line in FACT_CHECKS_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]
        if facts:
            return facts
    return DEFAULT_FACTS


def ingest_texts(texts: list[str]):
    embeddings = embed_texts(texts)
    ids = [str(uuid.uuid4()) for _ in texts]

    add_documents(
        ids=ids,
        texts=texts,
        embeddings=embeddings,
    )


if __name__ == "__main__":
    facts = load_fact_checks()
    ingest_texts(facts)
    print(f"Ingested {len(facts)} facts into the knowledge base")
