---
name: prepare-meeting
description: >
  Ghostwriter: prepares an upcoming meeting from the counterpart profiles already in
  memory on Notion — a realistic goal, what each person risks if they say yes,
  questions to ask, zero-cost symbolic concessions, topics to avoid, the order in
  which to talk to people. Use it when the user says "I'm seeing Mark tomorrow about
  the budget, how do I approach him?", "Monday I have the negotiation with the
  Farnsworth account", "I need to talk to my partners about the new product line,
  prepare me", "how do I set up the team meeting", "what should I expect from the
  meeting with the supplier". Read-only: writes nothing to Notion. To process a
  recording that already happened use process-meeting; to write a message use
  compose-message.
license: MIT
---

# Prepare a meeting

**Read-only. This skill writes nothing to Notion.**

References like `profiling-references:references/<file>.md` resolve to
`../profiling-references/references/<file>.md` relative to this skill's directory.

## Step 0 — Configuration

Load `profiling-references:references/core-rules.md`, then `configuration.md` from
the Ghostwriter home (`./.ghostwriter/` if it has one, otherwise `~/.ghostwriter/`),
then `profiling-references:references/execution-modes.md`. If `configuration.md` does
not exist: stop and point to `setup-notion-memory`. Reply in the user's language.

## Step 1 — Resolve the people and check the queue

Find the people named with the query in
`profiling-references:references/notion-queries.md`. Load **properties only**; the
page body only if you need to reread *Contradictions*. **Do not open past meetings.**

**Mandatory check:** query Meetings with filter `Participants contains <person>`
**and** `Status ≠ Processed`. If you find something, warn at the top of the output —
"you have an unprocessed recording from October 3 with this person" — and apply
**DP-5**.

For each person determine the **regime** (C/P/S/F) as in
`profiling-references:references/ethical-legal-limits.md` §1. If a person is in
`excluded`, do not proceed for them.

## Step 2 — Check whether you have enough material

Load `profiling-references:references/analysis-method.md`.

| `Profile reliability` | What you produce |
|---|---|
| **Low** (1 useful meeting) | **no strategy.** Only the factual observations you have and the list of questions to ask to verify them |
| **Medium** (2–4) | hypotheses declared as hypotheses, each with how to verify it |
| **High** (5+, no open contradiction) | full strategy |

This is not caution for show: a strategy built on one meeting is a riddle dressed up
as analysis, and acting on it costs more than not having it.

**Regime S:** no strategies of any kind. Produce the summary of what was decided,
what remained open, and the useful operational questions.

**Regime P:** no internal positioning strategies.

## Step 3 — Produce the output

Six blocks, in this order:

1. **Realistic goal** for this meeting — one, not three.
2. **What each person risks if they say yes** — the heart of the framing. For each
   person: what agreeing costs them personally, and whom they must justify
   themselves to.
3. **Three questions to ask**, in order.
4. **Two zero-cost symbolic concessions per person**, in the format of
   `analysis-method.md` §7. If there are none, write
   `no zero-cost concession identified`.
5. **What not to say** — topics that do not work or backfire.
6. **What to listen for** — and here **verbal content only**: which topics they
   raise, which they avoid, what they ask to come back to. No body or vocal signals,
   not even as advice: the system does not do that job, and does not do it by
   suggesting it to you either.

With several people add the **order of contacts**, derived from the `Influenced by` /
`Influences` relations: talk **first to whoever influences**, not to whoever
decides.

At the top of the output always show the **open predictions** on each person and
their historical hit rate (`analysis-method.md` §9). They serve two purposes: knowing
what the profile is betting on in this meeting, and knowing how far to trust it. A
rate under 40% means the profile is wrong, not incomplete.

## Step 4 — Declare what it rests on

Always close with the basis of the analysis, for each person *(fictional example)*:

```
Gorrand Mark — profile on 3 useful meetings, reliability Medium, last on October 3.
  Open contradictions: 1 (delivery times).
Farrowby Neil — regime S, limited profile: stated positions only.
```

And with the **links to the people's pages**, so corrections are made by hand where
they belong.

A profile built on one meeting must be said to be worth little, otherwise you will
use it as if it were worth a lot.
