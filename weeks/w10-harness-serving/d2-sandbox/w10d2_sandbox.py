"""W10 D2: path containment, command policy, bounded execution."""
import os
import shlex
import subprocess


class PathEscape(Exception):
    pass


def resolve_in_workspace(workspace: str, path: str) -> str:
    """Resolve path (relative paths are relative to workspace; absolute paths stay absolute) with realpath,
    and require it to be inside realpath(workspace) (commonpath). Return the resolved path or raise PathEscape."""
    ws = os.path.realpath(workspace)
    p = os.path.realpath(os.path.join(ws, path))
    if os.path.commonpath([ws, p]) != ws:
        raise PathEscape(path)
    return p


METACHARS = (";", "&&", "||", "|", "`", "$(", ">", "<", "\n")


class CommandPolicy:
    def __init__(self, allow: set, deny_args: dict):
        """allow: allowed executables. deny_args: executable -> set of forbidden argument tokens."""
        self.allow, self.deny_args = allow, deny_args

    def check(self, cmd: str) -> tuple:
        """Return (ok, reason, argv). Reasons (first that applies):
        "metachar" if any METACHARS substring is in cmd; "parse" if shlex fails; "empty" if no tokens;
        "not allowed: <exe>" if argv[0] not in allow; "denied arg: <arg>" for the first forbidden argument.
        On success: (True, "ok", argv)."""
        if any(m in cmd for m in METACHARS):
            return False, "metachar", []
        try:
            argv = shlex.split(cmd)
        except ValueError:
            return False, "parse", []
        if not argv:
            return False, "empty", []
        if argv[0] not in self.allow:
            return False, f"not allowed: {argv[0]}", argv
        for a in argv[1:]:
            if a in self.deny_args.get(argv[0], set()):
                return False, f"denied arg: {a}", argv
        return True, "ok", argv


def run_bounded(argv: list, cwd: str, timeout: float, max_output: int) -> dict:
    """subprocess.run without a shell, stdout+stderr combined (stderr=STDOUT), text mode.
    On timeout: {"exit": None, "output": "", "truncated": False, "timed_out": True}.
    Otherwise cap output at max_output characters; if capped append "\n[truncated]" and set truncated=True."""
    try:
        r = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"exit": None, "output": "", "truncated": False, "timed_out": True}
    out = r.stdout
    truncated = len(out) > max_output
    if truncated:
        out = out[:max_output] + "\n[truncated]"
    return {"exit": r.returncode, "output": out, "truncated": truncated, "timed_out": False}
