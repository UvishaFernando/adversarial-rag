from typing import Callable, List, Tuple


def retrieve(query: str, embed_fn: Callable, store, k: int = 5) -> List[Tuple[object, float]]:
    """
    embed_fn: a function(list[str]) -> np.ndarray, e.g. embedder.embed
    store: a VectorStore instance
    Returns list of (chunk, score) tuples, best first.
    """
    q_emb = embed_fn([query])[0]
    return store.search(q_emb, k=k)