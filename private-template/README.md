# Private material: format

Your real stories, numbers and case files go in a **separate private repo**
(suggested: `staff-prep-private`). This folder shows the format with one fully worked fictional
example per file, so you know exactly what to write. Sync with:

```bash
bash scripts/sync_private.sh ~/src/staff-prep-private
```

| File | What | Used in |
|---|---|---|
| `stories.json` | your STAR bank, machine-readable (W11 D5 computes coverage from it) | W11 D5, W12 D4 |
| `case-file.md` | one per major project: context, decisions, numbers, what you would do differently | W11, W12 D4 deep dive |
| `numbers.md` | every number you will say in an interview, with its source and how to re-derive it | all mocks |

Rule: if you cannot re-derive a number from raw data with your own code, you do not say it.
