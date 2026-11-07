"""Self-contained. Run after predict.md."""
import os
import shlex

ws = "/tmp/ws"
p = os.path.realpath(os.path.join(ws, "../ws-evil/x"))
print(f"1. resolved {p}: startswith -> {p.startswith(ws)} (WRONG), commonpath -> {os.path.commonpath([ws, p]) == ws}")
print("2.", shlex.split("grep foo a.txt; rm -rf /"),
      "-> argv[0] is grep, but with shell=True the ';' would run rm. Reject metacharacters; never use shell=True.")
print("3. it blows the context window and the budget; cap it (e.g. 10 KB) and say it was truncated")
