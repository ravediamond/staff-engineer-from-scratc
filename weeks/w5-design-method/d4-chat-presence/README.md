# W5 D4: chat: ordering, receipts, presence

Primer: `knowledge/05-design-method-and-estimation.md` §5.

## The one idea

Chat looks simple and hides three distributed-systems problems:

1. **Ordering.** Client clocks lie. The server assigns a **monotonic sequence number per
   conversation** (one writer per conversation: a partition owner or a DB sequence). Everyone
   renders by `seq`. Global ordering across conversations is not needed: do not pay for it.
2. **Duplicates.** Mobile clients retry. Each message carries a `client_msg_id`; the server returns
   the existing `seq` for a duplicate (W2 D3 again).
3. **Receipts.** "Read up to seq N" is a **monotonic pointer**: `read[user, conv] = max(old, N)`.
   Acks arrive out of order on flaky networks; a pointer that can move backwards resurrects
   unread badges.

**Presence:** clients heartbeat every ~30 s; a user is online if the last heartbeat is newer than a
timeout (~2 heartbeats). Never store "online = true" without expiry: crashed clients never send
"offline".

## Today's build (`w5d4_chat.py`)

`ChatService`: `send(conv, sender, client_msg_id, text) -> seq`, `fetch(conv, after_seq, limit)`,
`mark_read(user, conv, seq)`, `unread(user, conv)`. `Presence(timeout)`: `heartbeat(user, t)`,
`is_online(user, now)`, `online(users, now)`.

## Staff angle

The staff part of chat design is the connection layer and fan-out: millions of long-lived
WebSocket connections on gateway nodes, a routing table user → gateway, and delivery through a
pub/sub fabric. Design for gateway node loss (clients reconnect and resync from their last seq,
so the server never needs to know what was delivered, only what was acknowledged) and for
group chats of 100k members (switch to pull for large groups, the same hybrid as the feed).
