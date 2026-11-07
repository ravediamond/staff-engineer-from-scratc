# Drills: 48 problems, 4 per week, 15 minutes each

The coding rounds at Google and Meta are still LeetCode-shaped at staff level. The labs teach you to
build; the drills keep the pattern recognition fast. One drill = 15 minutes: 2 to restate and plan out
loud, 10 to code, 3 to test edge cases by hand. Then run the tests.

```bash
uv run pytest drills/w01 -k d01      # one drill
uv run pytest drills/w01             # the week
```

From week 5, do them as **timed pairs**: two drills, 35 minutes, no break (the real round format).
Log time and result in `PROGRESS.md` and the pattern in one line. Patterns: `PATTERNS.md`.

| Week | Pattern | Drills |
|---|---|---|
| 1 | hashing, prefix sums | d01 group anagrams · d02 longest consecutive · d03 product except self · d04 subarray sum = k |
| 2 | two pointers, sliding window | d05 most water · d06 longest unique substring · d07 minimum window substring · d08 trapping rain water |
| 3 | stacks, monotonic stacks, parsing | d09 daily temperatures · d10 largest rectangle · d11 evaluate RPN · d12 decode string |
| 4 | binary search, incl. on the answer | d13 rotated array search · d14 minimum eating speed · d15 median of two sorted arrays · d16 peak element |
| 5 | heaps | d17 merge k sorted · d18 kth largest stream · d19 employee free time · d20 maximise capital |
| 6 | graphs: backtracking, Bellman-Ford, union-find, topo | d21 word search · d22 cheapest flights k stops · d23 accounts merge · d24 alien dictionary |
| 7 | trees | d25 level order · d26 validate BST · d27 lowest common ancestor · d28 serialize/deserialize |
| 8 | 1-D dynamic programming | d29 house robber · d30 longest palindromic substring · d31 word break · d32 decode ways |
| 9 | 2-D DP and greedy | d33 unique paths with obstacles · d34 partition equal subset · d35 jump game II · d36 gas station |
| 10 | backtracking | d37 subsets · d38 permutations · d39 combination sum · d40 n-queens |
| 11 | design | d41 LFU cache · d42 min stack · d43 hit counter · d44 snapshot array |
| 12 | mixed hard | d45 sliding window median · d46 regex matching · d47 longest increasing path · d48 text justification |
