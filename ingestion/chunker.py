import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class Chunk:
    text: str
    source: str
    chunk_id: int
    metadata: dict = field(default_factory=dict)


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


HEADING_RE = re.compile(r"^(#{1,6}\s+.*|[A-Z][A-Za-z0-9 ]{2,60}:?\s*$)", re.MULTILINE)
BULLET_RE = re.compile(r"^\s*([-*•]|\d+\.)\s+", re.MULTILINE)


def split_into_structural_units(text: str) -> List[str]:
    # Normalize line endings, collapse 3+ newlines to 2 (paragraph breaks)
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    raw_units = [u.strip() for u in text.split("\n\n") if u.strip()]
    return raw_units


def pack_units(
    units: List[str],
    source: str,
    target_tokens: int = 400,
    overlap_tokens: int = 75,
) -> List[Chunk]:
    chunks: List[Chunk] = []
    current: List[str] = []
    current_tokens = 0
    chunk_id = 0

    def flush(carry_overlap: bool = True):
        nonlocal current, current_tokens, chunk_id
        if not current:
            return
        chunk_text = "\n\n".join(current)
        is_heading = bool(HEADING_RE.match(current[0])) if current else False
        is_bullets = bool(BULLET_RE.search(chunk_text))
        chunks.append(
            Chunk(
                text=chunk_text,
                source=source,
                chunk_id=chunk_id,
                metadata={"has_heading": is_heading, "has_bullets": is_bullets},
            )
        )
        chunk_id += 1

        if carry_overlap:
            overlap_units = []
            tok_count = 0
            for u in reversed(current):
                tok_count += estimate_tokens(u)
                overlap_units.insert(0, u)
                if tok_count >= overlap_tokens:
                    break
            current = overlap_units
            current_tokens = sum(estimate_tokens(u) for u in current)
        else:
            current = []
            current_tokens = 0

    for unit in units:
        unit_tokens = estimate_tokens(unit)

        if HEADING_RE.match(unit) and current:
            flush()

        if current_tokens + unit_tokens > target_tokens and current:
            flush()

        current.append(unit)
        current_tokens += unit_tokens

    flush(carry_overlap=False)
    return chunks


def chunk_document(
    text: str,
    source: str,
    target_tokens: int = 400,
    overlap_tokens: int = 75,
) -> List[Chunk]:
    units = split_into_structural_units(text)
    return pack_units(units, source, target_tokens, overlap_tokens)