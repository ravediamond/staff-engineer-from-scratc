# W15 D3: SQL under pressure

Primer: `knowledge/19-databases.md` §3.

## The one idea

Back Market, Doctolib, Qonto, Alan and most data-heavy loops put a schema in front of you and ask for
queries, live. The same six patterns cover nearly everything:

| Pattern | Tool |
|---|---|
| top-N per group | `ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)` in a CTE, filter `rn <= N` |
| running total, moving average | `SUM(…) OVER (PARTITION BY … ORDER BY … ROWS …)` |
| compare with the previous row | `LAG(…) OVER (…)` |
| rows with no match (anti-join) | `NOT EXISTS` (or `LEFT JOIN … WHERE right.id IS NULL`); never `NOT IN` on a nullable column |
| sessions / islands | `LAG` to flag a new group, running `SUM` of the flags as group id |
| conditional aggregates | `SUM(CASE WHEN … THEN 1 ELSE 0 END)`, `COUNT(*) FILTER (WHERE …)` |

Logical order of evaluation: `FROM/JOIN → WHERE → GROUP BY → HAVING → window functions → SELECT →
DISTINCT → ORDER BY → LIMIT`. That is why you cannot filter on a window function in `WHERE` (wrap it
in a CTE), and why `WHERE` on the right table of a `LEFT JOIN` turns it into an inner join.

## Today's build (`w15d3_sql.py`)

Six functions that each return **one SQL string**, run on SQLite in memory (`schema.py`, provided).
The last one also asks you for an index and checks the plan with `EXPLAIN QUERY PLAN`.

## Staff angle

Speak while you write: grain of each table ("one row per order item"), grain of the result, join
cardinality ("this join multiplies rows, so I aggregate before joining"), NULL behaviour. Wrong
results from join fan-out are the classic silent bug in metrics, and catching it out loud is the signal.
