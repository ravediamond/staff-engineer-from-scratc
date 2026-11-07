import os
import sys

import pytest

from w10d2_sandbox import CommandPolicy, PathEscape, resolve_in_workspace, run_bounded


def test_containment(tmp_path):
    ws = tmp_path / "work"
    ws.mkdir()
    (tmp_path / "work-evil").mkdir()
    (ws / "a.txt").write_text("x")
    assert resolve_in_workspace(str(ws), "a.txt") == os.path.realpath(ws / "a.txt")
    assert resolve_in_workspace(str(ws), "sub/../a.txt").endswith("a.txt")
    for bad in ["../work-evil/x", "/etc/passwd", "../../x"]:
        with pytest.raises(PathEscape):
            resolve_in_workspace(str(ws), bad)


def test_symlink_escape(tmp_path):
    ws = tmp_path / "work"
    ws.mkdir()
    os.symlink("/etc", ws / "link")
    with pytest.raises(PathEscape):
        resolve_in_workspace(str(ws), "link/passwd")


def test_policy():
    pol = CommandPolicy(allow={"ls", "grep", "git"}, deny_args={"git": {"push", "--force"}})
    assert pol.check("grep -n foo a.txt") == (True, "ok", ["grep", "-n", "foo", "a.txt"])
    assert pol.check("grep foo a.txt; rm -rf /")[:2] == (False, "metachar")
    assert pol.check("ls $(whoami)")[:2] == (False, "metachar")
    assert pol.check("rm -rf /")[:2] == (False, "not allowed: rm")
    assert pol.check("git push origin main")[:2] == (False, "denied arg: push")
    assert pol.check("grep 'unclosed")[:2] == (False, "parse")
    assert pol.check("   ")[:2] == (False, "empty")


def test_run_bounded(tmp_path):
    out = run_bounded([sys.executable, "-c", "print('x' * 100)"], str(tmp_path), timeout=10, max_output=20)
    assert out["exit"] == 0 and out["truncated"] and out["output"] == "x" * 20 + "\n[truncated]"
    out = run_bounded([sys.executable, "-c", "import time; time.sleep(5)"], str(tmp_path), timeout=0.5, max_output=20)
    assert out["timed_out"] and out["exit"] is None
    out = run_bounded([sys.executable, "-c", "import sys; sys.stderr.write('err'); sys.exit(3)"], str(tmp_path), 10, 100)
    assert out["exit"] == 3 and out["output"] == "err" and not out["truncated"]
