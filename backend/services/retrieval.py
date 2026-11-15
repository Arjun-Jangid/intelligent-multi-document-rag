
from rank_bm25 import BM25Okapi

from backend.services.vector_store import model, collection
from backend.services.reranking import rerank_documents


def retrieve_documents(query: str, top_k: int = 20):
    total_chunks = collection.count()

    if total_chunks == 0:
        return []


    query_embedding = model.encode(query).tolist()

    semantic_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, total_chunks),
        include=["documents", "metadatas", "distances"]
    )

    candidates = {}

    for chunk_id, document, metadata, distance in zip(
        semantic_results["ids"][0],
        semantic_results["documents"][0],
        semantic_results["metadatas"][0],
        semantic_results["distances"][0]
    ):
        candidates[chunk_id] = {
            "id": chunk_id,
            "text": document,
            "metadata": metadata,
            "distance": distance
        }


    all_chunks = collection.get(
        include=["documents", "metadatas"]
    )

    if all_chunks["documents"]:
        tokenized_corpus = [
            doc.lower().split()
            for doc in all_chunks["documents"]
        ]

        bm25 = BM25Okapi(tokenized_corpus)
        query_tokens = query.lower().split()

        scores = bm25.get_scores(query_tokens)

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        for index in top_indices:
            chunk_id = all_chunks["ids"][index]

            candidates[chunk_id] = {
                "id": chunk_id,
                "text": all_chunks["documents"][index],
                "metadata": all_chunks["metadatas"][index],
                "distance": None
            }


    retrieved_chunks = list(candidates.values())

    return rerank_documents(
        query,
        retrieved_chunks,
        top_n=4
    )
