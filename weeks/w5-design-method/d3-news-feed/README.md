# W5 D3: news feed: fan-out on write, on read, and hybrid

Primer: `knowledge/05-design-method-and-estimation.md` §4.

## The one idea

| Model | On post | On read | Breaks when |
|---|---|---|---|
| **Fan-out on write (push)** | write post id into every follower's inbox | read your inbox | an author has 50M followers: one post = 50M writes |
| **Fan-out on read (pull)** | write to author's outbox only | merge outboxes of everyone you follow | you follow 2,000 accounts: one read = 2,000 fetches |
| **Hybrid** | push for normal authors | pull only from the few "celebrities" you follow, merge | needs a threshold and a merge |

The merge is a k-way merge of lists already sorted by time **descending** (newest first),
truncated to N: a heap problem. Inboxes are capped (e.g. last 800 entries): nobody scrolls 10k items.

## Today's build (`w5d3_feed.py`)

`FeedService(celebrity_threshold, inbox_cap)`: `follow(a, b)`, `post(author, post_id, ts)` (push to
followers unless author is a celebrity; always append to author's outbox), `feed(user, n)` (inbox +
outboxes of followed celebrities + own posts, newest first, no duplicates), and counters `writes`,
`reads`. Plus `fanout_writes(follower_counts, threshold)`: inbox writes caused by one post from each author.

## Staff angle

At staff level the feed question becomes a ranking question: chronological feeds died around
2016. Candidate generation (the fan-out you just built) feeds a ranker (two-tower retrieval +
heavy ranker on a few hundred candidates), with freshness, diversity and integrity filters. A
staff answer separates the **candidate store** (this lab), the **ranking service** (an ML system
with its own latency budget, around 100 ms) and the **feedback loop** (impressions and engagement
logged back for training), and asks how ranking quality is evaluated online (W7 D4).
