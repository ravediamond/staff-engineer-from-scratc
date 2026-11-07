# Week 11: staff judgment and behavioral

The difference between senior and staff is rarely a data structure. It is: finding the real root
cause when three teams blame each other, refusing to claim something works without evidence,
writing the document that ends a month of debate, migrating a live system without an outage,
and telling the story of your work so the interviewer hears scope, not tasks. This week turns
each of those into a small tool you build and a habit you rehearse.

Primers: `knowledge/12-staff-rubrics.md` (what Meta, Google and Paris unicorns look for) and
`principal/README.md` (the next level, read on the weekend).

| Day | Lab | Review bug |
|---|---|---|
| d1 | root cause: flaky-aware bisect, change-point detection, deploy correlation | bisect returns the midpoint, not the boundary |
| d2 | prove it works: a property-based testing mini-framework with shrinking | shrinker reports the original, not the minimal case |
| d3 | design docs: a linter for your own RFCs | headings inside code blocks count as sections |
| d4 | live migrations: dual-write, resumable backfill, verify, gated cutover | cutover allowed before verification passes |
| d5 | STAR bank as data: validation, coverage against level rubrics, story picking | coverage counts stories with no measurable result |
