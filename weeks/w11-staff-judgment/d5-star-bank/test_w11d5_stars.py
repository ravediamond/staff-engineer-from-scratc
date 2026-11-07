from w11d5_stars import STAFF_SIGNALS, coverage, gaps, pick_story, validate_story

ACTION = ("Wrote a one-page RFC with two alternatives, built a 300-case eval set with stratified slices, calibrated "
          "an LLM judge against two annotators, ran shadow mode for four weeks, then made the gate blocking.")


def story(i, signals, result="Zero regressions in 2 quarters; review time 2 days to 2 hours.", action=ACTION):
    return {"id": f"s{i}", "title": "t", "situation": "s", "task": "t", "action": action, "result": result,
            "signals": signals}


def test_validate():
    assert validate_story(story(1, ["scope"])) == []
    s = story(2, ["scope", "heroics"], result="everyone was happy", action="I fixed it.")
    assert validate_story(s) == ["result needs a number", "action too short", "unknown signal heroics"]
    assert validate_story({"id": "x"})[:2] == ["missing title", "missing situation"]


def test_coverage_counts_only_valid():
    stories = [story(1, ["scope", "influence"]), story(2, ["influence"]), story(3, ["conflict"], result="it went well")]
    cov = coverage(stories, STAFF_SIGNALS)
    assert cov["influence"] == ["s1", "s2"] and cov["conflict"] == []
    assert gaps(cov, 2) == ["scope", "ambiguity", "technical-depth", "execution", "people-growth", "conflict"]


def test_pick_story():
    stories = [story(1, ["influence"]), story(2, ["influence", "conflict"], result="Cut costs 30% in 3 months."),
               story(3, ["influence", "conflict"], result="Shipped in 6 weeks, 2 teams adopted, 0 incidents, 140 daily users.")]
    assert pick_story(stories, ["conflict", "influence"])["id"] == "s3"
    assert pick_story(stories, ["ambiguity"]) is None
