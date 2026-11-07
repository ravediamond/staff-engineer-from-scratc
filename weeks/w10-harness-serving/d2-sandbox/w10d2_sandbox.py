"""W10 D2: path containment, command policy, bounded execution."""
import os
import shlex
import subprocess


class PathEscape(Exception):
    pass


def resolve_in_workspace(workspace: str, path: str) -> str:
    """Resolve path (relative paths are relative to workspace; absolute paths stay absolute) with realpath,
    and require it to be inside realpath(workspace) (commonpath). Return the resolved path or raise PathEscape."""
    # TODO
    raise NotImplementedError


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
        # TODO
        raise NotImplementedError


def run_bounded(argv: list, cwd: str, timeout: float, max_output: int) -> dict:
    """subprocess.run without a shell, stdout+stderr combined (stderr=STDOUT), text mode.
    On timeout: {"exit": None, "output": "", "truncated": False, "timed_out": True}.
    Otherwise cap output at max_output characters; if capped append "\n[truncated]" and set truncated=True."""
    # TODO
    raise NotImplementedError
