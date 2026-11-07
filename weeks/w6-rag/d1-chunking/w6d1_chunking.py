"""W6 D1: chunking strategies that keep (start, end) offsets into the source text."""
import re


def fixed_spans(text: str, size: int, overlap: int) -> list:
    """Windows of `size` chars with stride size - overlap. The last span ends at len(text).
    Do not emit a span that is entirely inside the previous one. Empty text -> []."""
    assert 0 <= overlap < size
    # TODO
    raise NotImplementedError


def recursive_spans(text: str, max_len: int, seps=("\n\n", "\n", ". ", " ")) -> list:
    """Contiguous spans covering text, each <= max_len unless a single unsplittable piece is longer.

    1. If len(text) <= max_len: one span.
    2. Else split on the first separator present in text (keep the separator at the END of each piece),
       recursively chunk any piece longer than max_len with the remaining separators,
    3. then greedily merge adjacent spans while the merged length stays <= max_len.
    Offsets are absolute (relative to the original text)."""
    # TODO
    raise NotImplementedError


def heading_chunks(md: str) -> list:
    """Split markdown at ATX headings (lines starting with 1-6 '#' then a space).
    Each chunk = a heading line through to the next heading (any level), as {"path", "start", "end"}.
    path = heading titles from the top level down to this heading, joined with " > ".
    Text before the first heading (if non-blank) is a chunk with path "".
    """
    # TODO
    raise NotImplementedError


def to_records(doc_id: str, text: str, spans: list) -> list:
    """[{"id": f"{doc_id}:{i}", "doc_id", "start", "end", "text"}] for spans given as (start, end)."""
    # TODO
    raise NotImplementedError
