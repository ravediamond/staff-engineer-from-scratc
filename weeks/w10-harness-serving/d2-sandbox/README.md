# W10 D2: sandbox: paths, commands, timeouts, output caps

Primer: `knowledge/10-harness-engineering.md` §2.

## The one idea

An agent with a shell is remote code execution by design. The harness must decide, **before**
running anything, whether it is allowed, and must bound what happens when it runs.

1. **Path containment.** Resolve the real path (`os.path.realpath`: follows `..` and symlinks), then
   check it is inside the workspace with `os.path.commonpath([ws, p]) == ws`. A string `startswith`
   check is wrong: `/work-evil` starts with `/work`.
2. **Command policy.** Parse with `shlex.split` (never `shell=True`), reject shell metacharacters you do
   not support (`;`, `&&`, `||`, `|`, `` ` ``, `$(`, `>`, `<`), allow-list executables, deny dangerous
   argument patterns.
3. **Execution bounds.** Timeout, output cap with an explicit truncation marker (so the model knows it
   did not see everything), working directory pinned to the workspace.

This is defence in depth on top of an OS sandbox (container, gVisor, Firecracker, seccomp), never instead of it.

## Today's build (`w10d2_sandbox.py`)

`resolve_in_workspace(ws, path)` (raises `PathEscape`), `CommandPolicy(allow, deny_args).check(cmd) -> (ok, reason, argv)`,
`run_bounded(argv, cwd, timeout, max_output)` → `{"exit", "output", "truncated", "timed_out"}`.

## Staff angle

The staff question is the threat model: who controls the input (the user, a web page the agent read,
a file in the repo: prompt injection), what is the blast radius (workspace only? network? credentials?),
and what is logged for audit. The policy in this lab is the last line, not the first: the first line is
an isolated execution environment with no ambient credentials.
