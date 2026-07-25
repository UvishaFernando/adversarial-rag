from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np


class BaseVectorStore(ABC):
    dim: int

    @abstractmethod
    def add(self, embeddings: np.ndarray, chunks: List) -> None:
        ...

    @abstractmethod
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[object, float]]:
        """Returns list of (chunk, similarity_score), best first."""

    @abstractmethod
    def save(self, dir_path: str) -> None:
        ...

    @classmethod
    @abstractmethod
    def load(cls, dir_path: str) -> "BaseVectorStore":
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...