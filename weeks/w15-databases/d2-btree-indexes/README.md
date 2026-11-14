# W15 D2: B+tree and index choice

Primer: `knowledge/19-databases.md` §2.

## The one idea

The default index of every relational database is a **B+tree**: a balanced tree with a high fan-out
(hundreds of keys per 8 KB page), all values in the **leaves**, and leaves **linked** left to right.

- Lookup: root to leaf, `log_fanout(n)` pages: 3–4 page reads for a billion rows.
- Range scan: find the first leaf, then follow the leaf links.
- Insert: put the key in its leaf; if the leaf overflows, **split** it and push a separator key into the
  parent, which may split in turn; when the root splits, the tree grows by one level. All leaves always
  stay at the same depth.

Compare with LSM (W4 D1): B-trees update in place (random writes, good reads, predictable latency);
LSM appends and compacts (fast writes, read and space amplification).

**Which index serves a query?** A composite index `(a, b, c)` is sorted by a, then b, then c. It can
be used for a **leftmost prefix**: equality on `a`; equality on `a, b`; equality on `a` and a range on
`b`. After the first range column the rest cannot narrow the scan. Rule of thumb for column order:
**equality columns first, then the range/sort column**. An index is **covering** when it contains
every column the query needs: the table is not touched at all (index-only scan).

## Today's build (`w15d2_btree.py`)

`BPlusTree(order)`: `search`, `insert`, `range`, `height`; `usable_prefix`, `is_covering`.

## Staff angle

"Add an index" is a senior answer. The staff answer names the access path: "equality on tenant_id,
range on created_at, so (tenant_id, created_at), and include status to make it covering; it costs a
write on every insert and we already have five indexes on this table".
