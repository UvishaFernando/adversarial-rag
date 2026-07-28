from retrieval.base_retriever import BaseRetriever

PRO_EXPANSION_TERMS = "benefits advantages positive evidence support strengths"


class ProRetriever(BaseRetriever):
    def expand_query(self, query: str) -> str:
        return f"{query} {PRO_EXPANSION_TERMS}"


def retrieve_pro(query: str, embed_fn, store, k: int = 5):
    return ProRetriever().retrieve(query, embed_fn, store, k=k)