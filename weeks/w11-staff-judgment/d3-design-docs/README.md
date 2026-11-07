# W11 D3: design docs that end debates

Primer: `knowledge/12-staff-rubrics.md` §4.

## The one idea

At staff level your highest-leverage artifact is the design doc (RFC): it turns a debate into a
decision others can execute without you. A good one has a fixed skeleton:

| Section | Must contain |
|---|---|
| Context | the problem in the reader's terms, with one number |
| Goals | 3–5, measurable |
| **Non-goals** | what you deliberately will not do (the most skipped, most valuable section) |
| Proposal | the design, one request walked end to end |
| **Alternatives considered** | at least 2 real options, with why not |
| Risks | what could go wrong, and the mitigation |
| Rollout | phases, flags, rollback |
| Metrics | how you will know it worked: numbers, not adjectives |

Today you build a linter for that skeleton and run it on your own RFC. Tools that check structure do
not judge quality; they free review time for the content.

## Today's build (`w11d3_doclint.py`)

`strip_code_blocks(md)`, `sections(md)` → `{title_lower: body}` for `##` headings outside code blocks,
`count_alternatives(body)` (bullets or `###` subheadings), `lint(md)` → list of issues.

Then write a real RFC (`my_rfc.md`, not committed if it contains employer material) for a problem you own
and make it lint-clean.

## Staff angle

Writing is how staff engineers scale. A design doc read by 40 people saves 40 meetings; a decision
log lets newcomers understand why the system looks the way it does. In interviews, "tell me about a
time you drove alignment" is answered best with "I wrote a doc with three options; here is the
trade-off table; here is what we chose and what happened".
