import random

from w6d1_chunking import fixed_spans, heading_chunks, recursive_spans, to_records

TEXT = ("Pump P-101 maintenance.\n\nCheck the seal every 500 hours. Replace the bearing if noise exceeds 80 dB.\n"
        "Safety: lock out the motor before opening.\n\nCompressor C-7 has a different procedure. "
        "Drain the condensate daily. Inspect valves weekly.")


def covers(spans, n):
    pos = 0
    for a, b in sorted(spans):
        if a > pos:
            return False
        pos = max(pos, b)
    return pos == n


def test_fixed_spans():
    t = "x" * 10_000
    s = fixed_spans(t, 1000, 200)
    assert len(s) == 13 and s[0] == (0, 1000) and s[1] == (800, 1800) and s[-1][1] == 10_000
    assert covers(s, len(t))
    assert fixed_spans("abc", 10, 2) == [(0, 3)]
    assert fixed_spans("", 10, 2) == []
    assert fixed_spans("a" * 20, 10, 0) == [(0, 10), (10, 20)]


def test_recursive_contiguous_and_bounded():
    s = recursive_spans(TEXT, 80)
    assert s[0][0] == 0 and s[-1][1] == len(TEXT)
    assert all(s[i][1] == s[i + 1][0] for i in range(len(s) - 1)), "contiguous, no overlap, no gap"
    assert all(b - a <= 80 for a, b in s)
    assert recursive_spans("short", 80) == [(0, 5)]


def test_recursive_prefers_paragraphs():
    s = recursive_spans(TEXT, 150)
    pieces = [TEXT[a:b] for a, b in s]
    assert pieces[0].startswith("Pump P-101") and pieces[0].endswith("\n\n")


def test_recursive_random_coverage():
    rng = random.Random(0)
    words = ["alpha", "beta", "gamma.", "delta\n", "eps\n\n", "zeta", "eta."]
    for _ in range(50):
        t = " ".join(rng.choice(words) for _ in range(rng.randint(1, 200)))
        s = recursive_spans(t, 60)
        assert s[0][0] == 0 and s[-1][1] == len(t)
        assert all(s[i][1] == s[i + 1][0] for i in range(len(s) - 1))


def test_heading_chunks_paths():
    md = "intro text\n# Pumps\nGeneral.\n## P-101\nSeal.\n## P-102\nBearing.\n# Compressors\nDrain.\n"
    ch = heading_chunks(md)
    assert [c["path"] for c in ch] == ["", "Pumps", "Pumps > P-101", "Pumps > P-102", "Compressors"]
    assert md[ch[2]["start"]:ch[2]["end"]] == "## P-101\nSeal.\n"
    assert ch[-1]["end"] == len(md)


def test_records():
    r = to_records("doc7", "hello world", [(0, 5), (6, 11)])
    assert r[1] == {"id": "doc7:1", "doc_id": "doc7", "start": 6, "end": 11, "text": "world"}
