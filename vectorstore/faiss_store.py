import pickle
from pathlib import Path
from typing import List, Tuple

import faiss
import numpy as np

from vectorstore.base_store import BaseVectorStore
from core.exceptions import VectorStoreError
from core.logger import get_logger

logger = get_logger(__name__)


class FaissVectorStore(BaseVectorStore):
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)  
        self.chunks: List = []  

    def add(self, embeddings: np.ndarray, chunks: List) -> None:
        if len(embeddings) != len(chunks):
            raise VectorStoreError(
                f"embeddings ({len(embeddings)}) and chunks ({len(chunks)}) must be the same length"
            )
        embeddings = np.asarray(embeddings, dtype="float32")
        self.index.add(embeddings)
        self.chunks.extend(chunks)
        logger.info(f"Added {len(chunks)} chunks (store now holds {len(self.chunks)})")

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[object, float]]:
        if len(self.chunks) == 0:
            raise VectorStoreError("Cannot search an empty vector store")
        q = np.asarray([query_embedding], dtype="float32")
        scores, indices = self.index.search(q, min(k, len(self.chunks)))
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.chunks[idx], float(score)))
        return results

    def save(self, dir_path: str) -> None:
        p = Path(dir_path)
        p.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(p / "index.faiss"))
        with open(p / "chunks.pkl", "wb") as f:
            pickle.dump(self.chunks, f)
        logger.info(f"Saved vector store ({len(self.chunks)} chunks) to {dir_path}")

    @classmethod
    def load(cls, dir_path: str) -> "FaissVectorStore":
        p = Path(dir_path)
        index = faiss.read_index(str(p / "index.faiss"))
        with open(p / "chunks.pkl", "rb") as f:
            chunks = pickle.load(f)
        store = cls(dim=index.d)
        store.index = index
        store.chunks = chunks
        return store

    def __len__(self) -> int:
        return len(self.chunks)

VectorStore = FaissVectorStore