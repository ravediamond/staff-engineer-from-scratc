from w11d3_doclint import count_alternatives, lint, sections, strip_code_blocks

GOOD = """# RFC: hybrid retrieval for the maintenance assistant

## Context
Recall@10 is 0.61 on identifier queries.

## Goals
- recall@10 >= 0.80 on identifier queries

## Non-goals
- changing the embedding model

## Proposal
Add BM25 and fuse with RRF.

```python
## Metrics
this heading is inside a code block and must be ignored
```

## Alternatives considered
### Fine-tune the embedder
Costly, slow to iterate.
### Query rewriting
Adds 300 ms.
### Do nothing
Baseline.

## Risks
Latency +20 ms.

## Rollout
Shadow mode for 2 weeks.

## Metrics
recall@10 on 300 identifier queries, p95 latency under 900 ms.
"""


def test_strip_and_sections():
    assert "inside a code block" not in strip_code_blocks(GOOD)
    s = sections(GOOD)
    assert list(s)[:3] == ["context", "goals", "non-goals"]
    assert "### Query rewriting" in s["alternatives considered"]
    assert s["metrics"].startswith("recall@10 on 300")


def test_count_alternatives():
    assert count_alternatives("### A\nx\n### B\ny\n### Do nothing\n") == 2
    assert count_alternatives("- option A\n- status quo\n  - nested detail\n") == 1


def test_good_doc_is_clean():
    assert lint(GOOD) == []


def test_issues():
    bad = "## Context\nx\n## Goals\ny\n## Non-goals\n\n## Proposal\nz\n## Alternatives considered\n- do nothing\n- A\n## Metrics\nfaster\n"
    assert lint(bad) == ["missing section: risks", "missing section: rollout", "non-goals is empty",
                         "need at least 2 alternatives", "metrics need numbers"]


def test_heading_only_in_code_block_is_missing():
    doc = GOOD.replace("## Metrics\nrecall@10 on 300 identifier queries, p95 latency under 900 ms.\n", "")
    assert "missing section: metrics" in lint(doc)
