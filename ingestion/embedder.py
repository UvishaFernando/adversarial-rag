from abc import ABC, abstractmethod
from typing import List
import numpy as np


class BaseEmbedder(ABC):
    dim: int

    @abstractmethod
    def embed(self, texts: List[str]) -> np.ndarray:
        ...


class LocalEmbedder(BaseEmbedder):

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_embedding_dimension()


    def embed(self, texts: List[str]) -> np.ndarray:
        return np.asarray(self.model.encode(texts, show_progress_bar=False, normalize_embeddings=True))


class OpenAIEmbedder(BaseEmbedder):


    def __init__(self, model_name: str = "text-embedding-3-small"):
        from openai import OpenAI

        self.client = OpenAI()
        self.model_name = model_name
        self.dim = 1536 if "small" in model_name else 3072

    def embed(self, texts: List[str]) -> np.ndarray:
        resp = self.client.embeddings.create(model=self.model_name, input=texts)
        vecs = [d.embedding for d in resp.data]
        return np.asarray(vecs, dtype="float32")


def get_embedder(backend: str = "local", **kwargs) -> BaseEmbedder:
    if backend == "local":
        return LocalEmbedder(**kwargs)
    if backend == "openai":
        return OpenAIEmbedder(**kwargs)
    raise ValueError(f"Unknown embedder backend: {backend}")