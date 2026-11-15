
import os
import chromadb
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "documents")

model = SentenceTransformer(EMBEDDING_MODEL)

client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

def store_chunks(chunks):
    if not chunks:
        return 0

    ids = [chunk["id"] for chunk in chunks]
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    embeddings = model.encode(texts).tolist()

    assert len(ids) == len(texts) == len(metadatas) == len(embeddings)

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)

