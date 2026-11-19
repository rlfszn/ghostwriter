---
name: compose-message
description: >
  Ghostwriter: writes a draft message (email, SMS, chat, internal message) or sets a
  strategy towards one or more profiled people, starting from their Notion profiles.
  Use it when the user says "write me a text for Barlow", "how do I tell him?",
  "prepare one email for the partners and one for the client", "what strategy do I
  use with Farnsworth and their engineer", "how do I get the workshop to accept the
  new shift", "answer this discount request for me". It only ever produces drafts to
  review: it sends nothing, publishes nothing, opens no mail client. With several
  recipients it produces variants consistent with each other and the order in which
  to contact them.
license: MIT
---

# Compose a message or a strategy

**This skill produces drafts. It does not send, publish or schedule anything** — in
any mode. It is not a preference: an automatic send based on a psychological profile
is exactly the kind of thing that must not be able to happen by mistake.

References like `profiling-references:references/<file>.md` resolve to
`../profiling-references/references/<file>.md` relative to this skill's directory.

## Step 0 — Configuration

Load `profiling-references:references/core-rules.md`, then `configuration.md` from
the Ghostwriter home (`./.ghostwriter/` if it has one, otherwise `~/.ghostwriter/`),
then `profiling-references:references/execution-modes.md`. If `configuration.md` does
not exist: stop and point to `setup-notion-memory`.

Talk to the user in their language. Write the **draft** in the language the user
asks for, or else the language they normally use with that recipient (from
`style.md` and the context).

## Step 1 — Resolve the recipients

Query from `profiling-references:references/notion-queries.md`. **Properties only**,
and of these you need: `Key drivers`, `Fears`, `Effective levers`, `Things to avoid`,
`Firm positions`, `Negotiable positions`, `Communication style`.

Determine each one's **regime**
(`profiling-references:references/ethical-legal-limits.md` §1) and their `Profile
reliability`.

| Constraint | Effect |
|---|---|
| `Reliability = Low` | no strategy: only a factual message and the questions to ask |
| regime **S** | only **operational** messages (what is needed, by when, with what information). No persuasion built on the profile |
| regime **P** | no internal positioning |
| person in `excluded` | do not proceed |

## Step 2 — Clarify the brief

From the request, or by asking if the mode is interactive: **channel** (SMS / chat /
email / internal message), **length**, **who must act after reading it, and how**.

Without the third element nothing is written: a message without an expected action is
a message without a shape.

## Step 3 — Build, in this order

Load `profiling-references:references/analysis-method.md` and
`profiling-references:references/ethical-legal-limits.md`.

For each recipient, **before** writing a line of text:

1. what they care about;
2. what they fear;
3. what the **zero-cost symbolic concession** is for them;

**then** write.

The order matters: writing first and justifying afterwards produces messages that
sound good and move nothing.

## Step 4 — The rules on the draft

Load `style.md` from the Ghostwriter home: it contains real examples of the user's
messages and their register constraints. **If it is missing or still unfilled, say
so** when closing: "draft in my register, not yours — `style.md` is not filled in".
A draft that has to be rewritten from scratch every time saves nobody any time.

- **Never quote the profile**, never mention the existence of the system.
- Do not use wording the user would not say out loud. The register comes from
  `style.md`; `preferences.draft_tone` is only the fallback.
- **A draft that "works" only because it exploits information the counterpart does
  not know they gave is not sent: it is rewritten.** It is the most important test of
  this skill.
- **Use only what that person said to the user or in their presence**, never what
  others reported about them, never dossier content.
- Apply the **reader test** of `ethical-legal-limits.md` §4 to the message itself: if
  the counterpart knew how it was built, would they find it unfair?
- Refuse what must be refused (`ethical-legal-limits.md` §5), in the format
  *"I won't do that: [reason]. I can instead [alternative]."*

## Step 5 — With several recipients, two more rules

1. **Cross-consistency check.** The variants must be able to sit side by side on the
   table without anyone feeling treated worse. Check it and **declare it**. In
   practice these people talk to each other: the email to the partners and the one
   to the production lead will end up being compared.
2. **Sequence and timing**: who receives first, who later, and why.

## Step 6 — Close

Always close with: **"Draft — reread before sending."** (in the user's language).

And with the basis it rests on: for each recipient, how many meetings the profile is
built on and its reliability.
