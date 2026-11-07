from w10d1_agent import ScriptedModel, Tool, run_agent, validate

READ = {"type": "object", "properties": {"path": {"type": "string"}, "max_lines": {"type": "integer"}},
        "required": ["path"], "additionalProperties": False}


def test_validate():
    assert validate(READ, {"path": "a.txt"}) == []
    assert validate(READ, {"pth": "a"}) == ["$.path: required", "$.pth: unexpected"]
    assert validate(READ, {"path": 3}) == ["$.path: expected string"]
    assert validate(READ, {"path": "a", "max_lines": True}) == ["$.max_lines: expected integer"]
    assert validate(READ, "nope") == ["$: expected object"]
    s = {"type": "array", "items": {"type": "string", "enum": ["a", "b"]}}
    assert validate(s, ["a", "c", 1]) == ["$[1]: not in enum", "$[2]: expected string"]


def tools():
    files = {"a.txt": "hello"}

    def read_file(path, max_lines=None):
        return files[path]

    def boom():
        raise TimeoutError("slow disk")

    return [Tool("read_file", READ, read_file), Tool("boom", {"type": "object", "properties": {}}, boom)]


def test_happy_path_and_trace():
    m = ScriptedModel([{"tool": "read_file", "args": {"path": "a.txt"}, "tokens": 10},
                       {"final": "it says hello", "tokens": 5}])
    out = run_agent(m, tools(), "what is in a.txt?", max_steps=5, max_tokens=100)
    assert out["status"] == "done" and out["answer"] == "it says hello"
    assert out["steps"] == 1 and out["tokens"] == 15
    assert out["trace"] == [{"tool": "read_file", "args": {"path": "a.txt"}, "observation": "hello"}]
    assert m.seen[1][-1] == {"role": "tool", "content": "hello"}


def test_errors_are_observations():
    m = ScriptedModel([{"tool": "read_file", "args": {"pth": "a.txt"}, "tokens": 1},
                       {"tool": "nope", "args": {}, "tokens": 1},
                       {"tool": "boom", "args": {}, "tokens": 1},
                       {"tool": "read_file", "args": {"path": "missing"}, "tokens": 1},
                       {"final": "gave up", "tokens": 1}])
    out = run_agent(m, tools(), "t", 10, 100)
    obs = [t["observation"] for t in out["trace"]]
    assert obs[0] == "error: invalid args: $.path: required; $.pth: unexpected"
    assert obs[1] == "error: unknown tool nope"
    assert obs[2] == "error: TimeoutError: slow disk"
    assert obs[3].startswith("error: KeyError")
    assert out["status"] == "done" and out["steps"] == 4


def test_budgets():
    loop = ScriptedModel([{"tool": "read_file", "args": {"path": "a.txt"}, "tokens": 10}])
    out = run_agent(loop, tools(), "t", max_steps=3, max_tokens=1000)
    assert out["status"] == "max_steps" and out["steps"] == 3 and len(out["trace"]) == 3
    loop2 = ScriptedModel([{"tool": "read_file", "args": {"path": "a.txt"}, "tokens": 40}])
    out = run_agent(loop2, tools(), "t", max_steps=100, max_tokens=100)
    assert out["status"] == "budget" and out["steps"] == 2
