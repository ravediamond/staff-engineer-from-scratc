import pytest

from w10d3_tracing import Recorder, Replayer, ReplayMismatch, Tracer, first_divergence, run_cost


def test_tracer_tree_and_duration():
    t = [0.0]
    tr = Tracer(lambda: t[0])
    run = tr.start("run", user="u1")
    m = tr.start("model", parent=run, tokens_in=1000, tokens_out=200)
    t[0] = 1.5
    tr.end(m, output="call search")
    tool = tr.start("tool", parent=run, tool_name="search")
    t[0] = 2.0
    tr.end(tool, status="error", output="timeout")
    tr.end(run)
    assert tr.children(run) == [m, tool]
    assert tr.duration(m) == 1.5 and tr.duration(run) == 2.0
    assert tr.spans[tool]["status"] == "error"
    assert run_cost(tr.spans, 3.0, 15.0) == pytest.approx(3.0 + 3.0)


def make_agent(call):
    def agent(question):
        a = call("search", q=question)
        b = call("search", q=question + " manual")
        return call("summarize", text=a + "|" + b)
    return agent


def test_record_then_replay_hermetic():
    real_calls = []
    tools = {"search": lambda q: real_calls.append(q) or f"results({q})",
             "summarize": lambda text: f"summary[{text}]"}
    rec = Recorder(tools)
    out1 = make_agent(rec.call)("pump")
    assert len(real_calls) == 2
    rep = Replayer(rec.recording)
    out2 = make_agent(rep.call)("pump")
    assert out2 == out1 == "summary[results(pump)|results(pump manual)]"
    assert len(real_calls) == 2, "replay must not touch real tools"


def test_replay_detects_behaviour_change():
    tools = {"search": lambda q: f"r({q})", "summarize": lambda text: "s"}
    rec = Recorder(tools)
    make_agent(rec.call)("pump")
    with pytest.raises(ReplayMismatch):
        make_agent(Replayer(rec.recording).call)("compressor")


def test_first_divergence():
    a = [{"tool": "search", "args": {"q": "x"}}, {"tool": "read", "args": {"p": 1}}]
    b = [{"tool": "search", "args": {"q": "x"}}, {"tool": "read", "args": {"p": 2}}]
    assert first_divergence(a, b) == 1
    assert first_divergence(a, a) is None
    assert first_divergence(a, a[:1]) == 1
