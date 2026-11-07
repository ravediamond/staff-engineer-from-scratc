"""W6 D5: ACL pre-filtering, lexical citation support, abstention, per-query cost."""
import re

STOPWORDS = {"the", "a", "an", "of", "to", "and", "or", "is", "are", "in", "on", "for", "with", "be", "it",
             "this", "that", "at", "by", "as", "from", "must", "should", "every"}


def content_words(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOPWORDS}


def acl_topk(scores: dict, acl: dict, user_groups: set, k: int) -> list:
    """scores: chunk -> similarity. acl: chunk -> set of groups allowed (missing = nobody).
    Keep only chunks sharing at least one group with the user, THEN take top-k by score desc (ties: id asc)."""
    allowed = [c for c in scores if acl.get(c, set()) & user_groups]
    return sorted(allowed, key=lambda c: (-scores[c], c))[:k]


def support_score(sentence: str, chunk_texts: list) -> float:
    """Fraction of the sentence's content words present in the union of the cited chunks' content words.
    1.0 if the sentence has no content words."""
    words = content_words(sentence)
    if not words:
        return 1.0
    pool = set().union(*(content_words(t) for t in chunk_texts)) if chunk_texts else set()
    return len(words & pool) / len(words)


def unsupported_sentences(answer: list, chunks: dict, threshold: float) -> list:
    """answer: [{"text": str, "cites": [chunk ids]}]. A sentence is unsupported if it cites nothing,
    cites an unknown chunk id, or its support_score < threshold. Return their indices."""
    bad = []
    for i, s in enumerate(answer):
        cites = s.get("cites", [])
        if not cites or any(c not in chunks for c in cites):
            bad.append(i)
        elif support_score(s["text"], [chunks[c] for c in cites]) < threshold:
            bad.append(i)
    return bad


def should_abstain(top_scores: list, threshold: float) -> bool:
    """Abstain if there are no results or the best score is below threshold."""
    return not top_scores or max(top_scores) < threshold


def query_cost(in_tokens: int, out_tokens: int, usd_per_m_in: float, usd_per_m_out: float,
               embed_tokens: int = 0, usd_per_m_embed: float = 0.0) -> float:
    """Dollars for one query."""
    return (in_tokens * usd_per_m_in + out_tokens * usd_per_m_out + embed_tokens * usd_per_m_embed) / 1e6
