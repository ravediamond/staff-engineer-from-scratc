"""W10 D1: agent loop with schema validation, errors as observations, and budgets."""
from dataclasses import dataclass, field

_TYPES = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "array": list, "object": dict}


def validate(schema: dict, value, path: str = "$") -> list:
    """Return a list of error strings (empty = valid). Rules:
    - type check (bool is NOT an integer or number); message f"{path}: expected {type}"; stop checking this node on type error
    - enum: f"{path}: not in enum"
    - object: each missing required key -> f"{path}.{key}: required"; with additionalProperties false, each extra key
      -> f"{path}.{key}: unexpected"; recurse into known properties (sorted key order for determinism)
    - array: recurse into items with path f"{path}[{i}]"
    Order: type, enum, required (sorted), unexpected (sorted), properties (sorted), items (in order)."""
    errs = []
    t = schema.get("type")
    if t is not None:
        py = _TYPES[t]
        ok = isinstance(value, py) and not (t in ("integer", "number") and isinstance(value, bool))
        if not ok:
            return [f"{path}: expected {t}"]
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path}: not in enum")
    if t == "object":
        props = schema.get("properties", {})
        for k in sorted(schema.get("required", [])):
            if k not in value:
                errs.append(f"{path}.{k}: required")
        if schema.get("additionalProperties") is False:
            for k in sorted(value):
                if k not in props:
                    errs.append(f"{path}.{k}: unexpected")
        for k in sorted(props):
            if k in value:
                errs += validate(props[k], value[k], f"{path}.{k}")
    if t == "array" and "items" in schema:
        for i, item in enumerate(value):
            errs += validate(schema["items"], item, f"{path}[{i}]")
    return errs


@dataclass
class Tool:
    name: str
    schema: dict
    fn: object


@dataclass
class ScriptedModel:
    """Provided: returns pre-scripted actions in order, ignoring messages. Each action is a dict with "tokens" and
    either {"tool", "args"} or {"final"}."""
    actions: list
    calls: int = 0
    seen: list = field(default_factory=list)

    def __call__(self, messages: list) -> dict:
        self.seen.append(list(messages))
        a = self.actions[min(self.calls, len(self.actions) - 1)]
        self.calls += 1
        return a


def run_agent(model, tools: list, task: str, max_steps: int, max_tokens: int) -> dict:
    """messages starts as [{"role": "user", "content": task}]. Loop:
      1. if steps == max_steps: stop with status "max_steps"
      2. action = model(messages); tokens += action["tokens"]; if tokens > max_tokens: stop with status "budget"
      3. "final" in action -> status "done", answer = action["final"]
      4. else steps += 1 (a tool step counts even if it fails); observation =
           unknown tool         -> "error: unknown tool <name>"
           validation errors    -> "error: invalid args: " + "; ".join(errors)
           tool raises e        -> f"error: {type(e).__name__}: {e}"
           otherwise            -> str(tool.fn(**args))
         append {"role": "assistant", "content": action} and {"role": "tool", "content": observation} to messages,
         append {"tool", "args", "observation"} to trace.
    Return {"status", "answer" (None unless done), "steps", "tokens", "trace"}."""
    by_name = {t.name: t for t in tools}
    messages = [{"role": "user", "content": task}]
    trace, steps, tokens = [], 0, 0
    while True:
        if steps == max_steps:
            return {"status": "max_steps", "answer": None, "steps": steps, "tokens": tokens, "trace": trace}
        action = model(messages)
        tokens += action["tokens"]
        if tokens > max_tokens:
            return {"status": "budget", "answer": None, "steps": steps, "tokens": tokens, "trace": trace}
        if "final" in action:
            return {"status": "done", "answer": action["final"], "steps": steps, "tokens": tokens, "trace": trace}
        steps += 1
        name, args = action["tool"], action.get("args", {})
        tool = by_name.get(name)
        if tool is None:
            obs = f"error: unknown tool {name}"
        else:
            errors = validate(tool.schema, args)
            if errors:
                obs = "error: invalid args: " + "; ".join(errors)
            else:
                try:
                    obs = str(tool.fn(**args))
                except Exception as e:
                    obs = f"error: {type(e).__name__}: {e}"
        messages.append({"role": "assistant", "content": action})
        messages.append({"role": "tool", "content": obs})
        trace.append({"tool": name, "args": args, "observation": obs})
