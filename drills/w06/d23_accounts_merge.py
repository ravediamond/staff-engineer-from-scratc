"""d23 Accounts merge: accounts = [[name, email1, email2, ...]]. Merge accounts sharing any email.
Return [[name, *sorted emails]] sorted by (name, first email)."""


def accounts_merge(accounts: list) -> list:
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    owner = {}
    for acc in accounts:
        name, emails = acc[0], acc[1:]
        for e in emails:
            owner[e] = name
            parent[find(e)] = find(emails[0])
    groups = {}
    for e in owner:
        groups.setdefault(find(e), []).append(e)
    return sorted([[owner[es[0]], *sorted(es)] for es in groups.values()], key=lambda a: (a[0], a[1]))
