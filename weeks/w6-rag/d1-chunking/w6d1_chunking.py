"""W6 D1: chunking strategies that keep (start, end) offsets into the source text."""
import re


def fixed_spans(text: str, size: int, overlap: int) -> list:
    """Windows of `size` chars with stride size - overlap. The last span ends at len(text).
    Do not emit a span that is entirely inside the previous one. Empty text -> []."""
    assert 0 <= overlap < size
    n, step, spans, start = len(text), size - overlap, [], 0
    while start < n:
        end = min(start + size, n)
        spans.append((start, end))
        if end == n:
            break
        start += step
    return spans


def recursive_spans(text: str, max_len: int, seps=("\n\n", "\n", ". ", " ")) -> list:
    """Contiguous spans covering text, each <= max_len unless a single unsplittable piece is longer.

    1. If len(text) <= max_len: one span.
    2. Else split on the first separator present in text (keep the separator at the END of each piece),
       recursively chunk any piece longer than max_len with the remaining separators,
    3. then greedily merge adjacent spans while the merged length stays <= max_len.
    Offsets are absolute (relative to the original text)."""
    def rec(lo, hi, seps):
        if hi - lo <= max_len:
            return [(lo, hi)]
        seg = text[lo:hi]
        for i, sep in enumerate(seps):
            if sep in seg:
                pieces, pos = [], 0
                for m in re.finditer(re.escape(sep), seg):
                    pieces.append((lo + pos, lo + m.end()))
                    pos = m.end()
                if pos < len(seg):
                    pieces.append((lo + pos, hi))
                out = []
                for a, b in pieces:
                    out += rec(a, b, seps[i + 1:]) if b - a > max_len else [(a, b)]
                return out
        return [(lo, hi)]

    if not text:
        return []
    merged = []
    for a, b in rec(0, len(text), tuple(seps)):
        if merged and b - merged[-1][0] <= max_len:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


def heading_chunks(md: str) -> list:
    """Split markdown at ATX headings (lines starting with 1-6 '#' then a space).
    Each chunk = a heading line through to the next heading (any level), as {"path", "start", "end"}.
    path = heading titles from the top level down to this heading, joined with " > ".
    Text before the first heading (if non-blank) is a chunk with path "".
    """
    heads = [(m.start(), len(m.group(1)), m.group(2).strip()) for m in re.finditer(r"^(#{1,6}) (.*)$", md, re.M)]
    out = []
    if not heads:
        return [{"path": "", "start": 0, "end": len(md)}] if md.strip() else []
    if md[: heads[0][0]].strip():
        out.append({"path": "", "start": 0, "end": heads[0][0]})
    stack = []
    for i, (pos, level, title) in enumerate(heads):
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, title))
        end = heads[i + 1][0] if i + 1 < len(heads) else len(md)
        out.append({"path": " > ".join(t for _, t in stack), "start": pos, "end": end})
    return out


def to_records(doc_id: str, text: str, spans: list) -> list:
    """[{"id": f"{doc_id}:{i}", "doc_id", "start", "end", "text"}] for spans given as (start, end)."""
    return [{"id": f"{doc_id}:{i}", "doc_id": doc_id, "start": a, "end": b, "text": text[a:b]}
            for i, (a, b) in enumerate(spans)]
