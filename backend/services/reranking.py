from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_documents(query, documents, top_n=4):
    if not documents:
        return []

    pairs = [
        (query, doc["text"])
        for doc in documents
    ]

    scores = reranker.predict(pairs)

    for doc, score in zip(documents, scores):
        doc["rerank_score"] = float(score)

    documents.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return documents[:top_n]