from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class RawDocument:
    text: str
    source: str                 
    metadata: dict = field(default_factory=dict)


def load_txt(path: str) -> RawDocument:
    p = Path(path)
    text = p.read_text(encoding="utf-8", errors="ignore")
    return RawDocument(text=text, source=p.name, metadata={"type": "txt"})


def load_pdf(path: str) -> RawDocument:
    try:
        from pypdf import PdfReader
    except ImportError as e:
        raise ImportError("pip install pypdf to load PDF files") from e

    p = Path(path)
    reader = PdfReader(str(p))
    pages = []
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        pages.append(page_text)
    text = "\n".join(pages)
    return RawDocument(
        text=text,
        source=p.name,
        metadata={"type": "pdf", "num_pages": len(reader.pages)},
    )


def load_document(path: str) -> RawDocument:
    ext = Path(path).suffix.lower()
    if ext == ".txt":
        return load_txt(path)
    if ext == ".pdf":
        return load_pdf(path)
    raise ValueError(f"Unsupported file type: {ext}")


def load_directory(dir_path: str) -> List[RawDocument]:
    docs = []
    for p in Path(dir_path).glob("*"):
        if p.suffix.lower() in (".txt", ".pdf"):
            docs.append(load_document(str(p)))
    return docs