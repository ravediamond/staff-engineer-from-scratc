"""Review: file tool path check. A security review found the agent could read files outside the workspace.
Find the bug, fix it, explain:

WHY:
"""
import os


def safe_path(workspace, path):
    ws = os.path.realpath(workspace)
    p = os.path.realpath(os.path.join(ws, path))
    if os.path.commonpath([ws, p]) != ws:
        raise PermissionError(path)
    return p
