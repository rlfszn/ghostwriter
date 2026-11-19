---
name: consult-profile
description: >
  Ghostwriter: answers questions about the counterpart profiles already in memory on
  Notion — who a person is, what they care about, what they fear, how the history of
  meetings went, who influences whom, which positions they took, which
  contradictions are open. Use it when the user asks "what do we know about
  Farnsworth?", "give me Barlow's profile", "who really counts at Gorrand's
  company?", "how many times have I seen that supplier?", "which contradictions did I
  note on my uncle", "list the skeptical clients", "whom have I profiled in the
  production team". Read-only: writes and modifies nothing. To prepare an upcoming
  meeting use prepare-meeting.
license: MIT
---

# Consult a profile

**Read-only. Zero writes, zero changes.**

References like `profiling-references:references/<file>.md` resolve to
`../profiling-references/references/<file>.md` relative to this skill's directory.

## Step 0 — Configuration

Load `profiling-references:references/core-rules.md`, then `configuration.md` from
the Ghostwriter home (`./.ghostwriter/` if it has one, otherwise `~/.ghostwriter/`),
then `profiling-references:references/notion-queries.md`. If `configuration.md` does
not exist: stop and point to `setup-notion-memory`. Reply in the user's language.

## Step 1 — Recognise the shape of the question

Three shapes, three recipes. Choosing the right one is the difference between an
answer and a saturated context.

| Question | Query | What you read |
|---|---|---|
| **"who is X"** | name/alias filter | properties, **then** the page body only if the user digs deeper |
| **"list of who is Y"** (e.g. "the skeptical clients") | filter `Category` + `Alignment with me`, limit 25 | **properties only**, no page body |
| **"who counts at Z"** | filter `Organization contains` | properties, then the `Influences` / `Influenced by` relations **as names**, without opening those pages |

For questions about the history ("how many times have I seen him", "how did it go
over time"): use the `Meeting count` and `Last meeting` rollups and the **history**
inside the Person page. **Do not open the Meeting pages** one by one: the history is
exactly the compressed record, and that is why it exists.

To read the whole archive (beyond 100 people) use view mode on the `Index` view,
paging.

Apply the decay rules on read (the windows are in
`profiling-references:references/analysis-method.md` §4; load it only for this): a claim past its window is
shown as `(to re-verify — last <date>)`, not as current.

## Step 2 — Present

- The **history is shown most recent first**, even though on Notion it is stored in
  ascending order.
- Show the **open contradictions** when there are any: they are the most useful part
  of the profile, not a defect to hide.
- If the user asks *why* the agent thinks something, show the quote and the meeting it
  comes from. If a claim has no evidence, say so.
- Never produce rankings or comparisons between people, in particular between members
  of the user's team (`ethical-legal-limits.md` §5): a list answers a filter, it does
  not rank.

## Step 3 — Always declare what it rests on

Every answer closes with the basis of the analysis *(fictional example)*:

```
Profile on 3 useful meetings · reliability Medium · last on October 3, 2026
Regime: C (counterparty) · 1 open contradiction
→ <link to the Person page>
```

**A profile built on one meeting must be said to be worth little**, otherwise the
user will use it as if it were worth a lot. This line is not an ornament: it is what
stops the system from looking surer than it is.

Close with the link to the page, so corrections are made by hand where they belong.
