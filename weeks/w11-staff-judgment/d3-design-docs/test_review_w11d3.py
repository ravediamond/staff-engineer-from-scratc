from review_w11d3 import has_section


def test_review_ignore_code_blocks():
    doc = "## Proposal\ntext\n```md\n## Rollout\nexample\n```\n"
    assert not has_section(doc, "Rollout")
    assert has_section(doc, "Proposal")
