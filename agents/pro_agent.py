from typing import Callable, List

from prompts.pro_prompt import PRO_PROMPT
from schemas.evidence import Evidence


def format_context(evidence: List[Evidence]) -> str:
    """evidence: list of Evidence objects, best (highest similarity) first."""
    lines = []
    for i, e in enumerate(evidence, start=1):
        score_label = e.strength_score if e.strength_score is not None else e.similarity_score
        lines.append(f"[{i}] (source: {e.source}, score: {score_label:.3f})\n{e.text}")
    return "\n\n".join(lines)


def run_pro_agent(query: str, evidence: List[Evidence], llm: Callable[[str], str]) -> str:
    context = format_context(evidence)
    prompt = PRO_PROMPT.format(query=query, context=context)
    return llm(prompt)