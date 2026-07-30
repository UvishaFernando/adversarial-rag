from abc import ABC, abstractmethod
from typing import Callable, List
from schemas.evidence import Evidence


class BaseRetriever(ABC):
    @abstractmethod
    def expand_query(self, query: str) -> str:
        """Return the (possibly biased) query string used for embedding + search."""

    def retrieve(self, query: str, embed_fn: Callable, store, k: int = 5) -> List[Evidence]:
        from schemas.evidence import evidence_from_chunk

        expanded = self.expand_query(query)
        q_emb = embed_fn([expanded])[0]
        results = store.search(q_emb, k=k)
        return [evidence_from_chunk(chunk, score) for chunk, score in results]