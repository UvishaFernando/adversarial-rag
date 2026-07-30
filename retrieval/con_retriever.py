from retrieval.base_retriever import BaseRetriever

CON_EXPANSION_TERMS = "risks disadvantages problems criticisms limitations against"


class ConRetriever(BaseRetriever):
    def expand_query(self, query: str) -> str:
        return f"{query} {CON_EXPANSION_TERMS}"


def retrieve_con(query: str, embed_fn, store, k: int = 5):
    return ConRetriever().retrieve(query, embed_fn, store, k=k)