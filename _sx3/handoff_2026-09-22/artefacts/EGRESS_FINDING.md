# Container limit measured 2026-09-22 14:17 UTC — served-site egress denied

The agent proxy now refuses CONNECT to the served host:

```
try 1: 000
try 2: 000
try 3: 000
```

`curl -sS "$HTTPS_PROXY/__agentproxy/status"` reports:

```
{"ts":"2026-09-22T14:17:07.778Z","kind":"connect_rejected",
 "detail":"gateway answered 403 to CONNECT (policy denial or upstream failure)",
 "host":"mattroper1977.github.io:443"}
```

Also denied earlier in the session:

```
{"ts":"2026-09-22T12:57:35.148Z","kind":"connect_rejected",
 "host":"results-receiver.actions.githubusercontent.com:443"}
```

## What this does and does not block

- **Blocks**: the 390 px served proof on the 21 Summer 1 responsive pages, and any other
  proof that fetches the live site. It is a container egress policy, not a product fault.
  It worked earlier this session (the title served proof, 12:10 UTC), so the policy or the
  allowlist changed mid-session.
- **Does not block**: the landing. Publication SUCCESS is still provable by run id through
  the GitHub API, which the proxy still allows.

Recorded as a container limit, not a pass. The served proof is OWED, not done.

## Served URL shape (derived, for when egress returns)

Mount derived from `domain-split/usage_discovery.py:143`:

```python
for part,prefix in [('education-site','/'),('education-lessons','/Lessons/'),('education-apps','/Matt-s-Apps-/')]:
```

So a published path `P` in `trees.education-lessons` serves at `https://mattroper1977.github.io/Lessons/P`.
The 21 HTML pages are the 27 admitted paths minus the 3 CHANGELOG.txt and 3 SHA256SUMS.txt.
