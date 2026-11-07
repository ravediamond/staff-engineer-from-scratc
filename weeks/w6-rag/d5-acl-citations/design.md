# Friday design #2: enterprise RAG platform

**Timer: 45 minutes. Write in `my_design.md`. Use the 45-minute frame.**

## Prompt

A 60,000-person industrial company wants an internal assistant answering questions from
SharePoint, Confluence, a document management system (maintenance procedures, safety sheets,
PDFs with tables and scanned drawings) and a ticketing system. 10,000 active users in the first
year, 9 languages. Documents have per-site and per-role permissions. Wrong answers on safety
procedures are a serious risk. The CFO wants a cost per query and a reason to believe it is worth it.

Design the platform.

## What the interviewer will push on

- Permissions: how are they mirrored, enforced, and kept fresh? What is the leak risk?
- How do you know answers are right, before launch and every week after?
- Safety-critical content: what is different?
- Cost per query and what dominates it. What would you cut first?
- Multi-tenancy: one index or many? Per-site?
- What would you not build in v1?

## Deliverable

Requirements and non-goals · estimation · API and data model · architecture with one request end
to end · two deep dives · metrics, risks, scope.
