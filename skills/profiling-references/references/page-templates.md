# Page templates

The headings are **stable anchors**: the agent looks them up by name, not by
position. Do not rename them, do not reorder them.

Headings and fixed labels below are in English. If the user's language is not
English, you may write the **content** in their language, but keep the heading
anchors exactly as written here: they are looked up by name. *(All names in the
examples are fictional.)*

## Person page

The first block is a callout with the disclaimer, used **verbatim** (translated into
the user's language if it is not English), with the regime filled in (see
`ethical-legal-limits.md` §1):

```markdown
> ⚠️ **Personal negotiation notes — regime: <C Counterparty | P Peer-Superior | S Subordinate | F Family>**
> This is not a professional evaluation and not a company document. It **may not be
> used** for decisions on hiring, pay, grade, duties, promotion, disciplinary
> measures or termination, nor shared with third parties.
> It contains **subjective inferences** drawn from the text of meetings I took part
> in, not established facts: they may be incomplete or wrong. No analysis of voice,
> tone or emotions.
> Data controller: **<me.name>**, a natural person, for personal use.
> At the request of the person concerned this page is shown in full and, if
> requested, deleted. Contact: **<me.contact_email>**.
```

The regime in the disclaimer is not decorative: it is how the agent, at the next
consultation, knows which fields it may touch without recomputing it.

```markdown
## Summary
(exactly 5 lines: who they are, what they want, what they fear, how they decide, how to talk to them)

## Extended analysis
(analysis with the textual evidence)

## Contradictions / to verify
(list; if empty, the section keeps the line "- none")

## Open predictions
(checkbox list; see below)

## History
(entries in ASCENDING chronological order, most recent at the bottom)
```

### Why the history is the last section, and grows downwards

It is not an aesthetic choice. The only available append primitive adds content **at
the end of the page** without having to read it first. If the history were not last,
every write would require rereading the page just to find the anchor to insert at:
one extra call, every time, for nothing.

Compensation: when you show the history to the user, **show it most recent first**.
The order on disk and the reading order need not match.

### Format of a prediction

Predictions live in the `## Open predictions` section, as checkbox list items. On
closing, the line **leaves** this section and becomes a dated history entry, with the
outcome and the quote that proves it.

```markdown
- [ ] P-2026-10-07-01 | Gideon Varro
      IF I bring Quadrel into production on ten units at the plenary meeting without
      first having given him the test-cycle data,
      THEN he will not object on technical merit but will make his opinion conditional
      on further checks and will ask that the decision be recorded in writing as not his.
      REFUTED IF: he gives a favourable opinion in the meeting itself, or objects on
      the technical merit of the component.
      Deadline: 2026-11-30 (or next production meeting, if earlier)
      Confidence: medium | Basis: meeting 2026-10-07, turns [T3] [T9] [T14]
```

Mandatory fields: ID `P-YYYY-MM-DD-NN`, person, condition (IF), expected behaviour
(THEN), **explicit refutation condition**, deadline, confidence, basis with turn
references.

**The text of a prediction is never modified after being written.** The acceptance
and closing rules are in `analysis-method.md` §9.

### Format of a history entry

A single list block, five mandatory fields, cap `max_chars_history_entry` (600):

```markdown
- **2026-10-07** · <mention-page url="https://www.notion.so/<MEETING_ID>">Gorrand negotiation — 3 conveyor lines</mention-page> · `MTG:plaud:7f3a9c` · **Changed:** `Fears` + a second safety inspection before go-live; `Negotiable positions` price negotiable against volumes. · **Evidence:** asks twice "and what if the inspector sends it back" [T22 | 11:40]; gives way on price only after the three-line scenario [T41 | 24:03]. · **Confidence:** medium.
```

| Field | Content | Why |
|---|---|---|
| **Date** | `YYYY-MM-DD`, the date of the **meeting** | ordering and correlation |
| **Meeting** | `<mention-page>` to the Meeting page | the link to the full evidence |
| **Anchor** | `MTG:<Recording ID>` | keeps the entry traceable outside Notion too. The idempotency receipt is the `Profiles processed` relation, not this |
| **Changed** | which properties changed and how, naming them | makes the update auditable |
| **Evidence** | short quote with anchor `[Tn \| mm:ss]` | mandatory. Without evidence the entry is not written. |
| **Confidence** | `high` / `medium` / `low` | flags where not to trust |

### Formal constraints

- **`<mention-page>` and not `<page>`.** A `<page>` tag with the URL of an existing
  page **moves** it inside the current page, and removing the tag deletes the child
  page. A `<page>` here would drag the meeting into the profile. `<mention-page>` is a
  harmless inline reference.
- **Two references, two purposes.** The `<mention-page>` is the clickable link; the
  `MTG:<Recording ID>` is plain text, so the entry stays readable and traceable in an
  export, in a diff or if the link breaks. **Neither is the idempotency receipt:**
  that is the `Profiles processed` relation on the Meeting, because the page body is
  rewritten by compaction and a text receipt would sooner or later disappear.
- **Characters to escape** in free text: `\ * ~ \` $ [ ] < > { } | ^`. A transcript
  regularly contains square brackets (`[inaudible]`) and angle brackets. Not escaping
  them breaks the block or, worse, produces interpreted tags.

### The history must not grow for ever

> The body of the Person page is a **bounded** document, of stable size over time.
> The unbounded log is the Meetings database.

No information is lost: every entry contains the link to the Meeting, which keeps the
full briefing and the transcript. The history is an **index**, not an archive.

**Compaction rule.** When the entries in full exceed `history_entries_in_full` (15),
compress the oldest `entries_to_compact` (5) into **one** archive line and remove them
from the full list:

```markdown
- **2025-01 → 2025-06** · *(6 meetings compacted)* Consolidated: drivers Control and Financial result; openness on delivery times, closed on regional exclusivity. · `MTG:plaud:1a2b` `MTG:plaud:3c4d` `MTG:plaud:5e6f` `MTG:plaud:7g8h` `MTG:plaud:9i0j` `MTG:plaud:1k2l`
```

### Anchors survive compaction, and it is not a detail

The archive line **must list all the `MTG:` anchors of the entries it compacted.** If
it does not, compaction destroys the traceability of the history: reprocessing an old
recording would no longer find its anchor in the body, and anyone checking by text
would believe the person was never written for that meeting — inventing a useful
meeting that does not exist and skewing the profile's reliability.

Six anchors cost about sixty characters. Six history entries cost 2,700. The saving
stays almost intact, and the textual cross-check keeps working as a simple search over
the whole section.

Compaction happens **after** the new entry has been appended, as a separate
operation, and only if the threshold is exceeded. That way the normal path stays a
single write.

With these numbers the body of a Person page stabilises at around 10–12 KB
**whatever the number of meetings**: a profile with 80 meetings behind it costs as
much to read as one with 15.

## Meeting page

```markdown
## Factual summary
(3–6 lines: decisions, numbers, commitments, deadlines. [FACT] only.)

## Prediction outcomes
(for each open prediction on the participants: CONFIRMED | REFUTED | PARTIAL |
LAPSED, with the quote that proves it. "No open predictions" if that is the case.)

## Briefing
### <Person name> (<Relationship>)
- What emerged: [STATED]/[FACT] with quotes
- What changes compared with the profile: confirmation | contradiction | new | nothing
- What in this meeting contradicts the current profile: … (or "nothing", explicitly)
- ToM: the P5 block

### <Person name 2> (<Relationship>)
(same)

## Dynamics
(who proposed, who gave way, who blocked, visible alliances, with quotes.
Who was present without speaking.)

## Recommended move
(one move only, max 3 lines: to whom, what, by when, and what not to do)

## Follow-up draft
(ready text, in the user's register, no reference to the profile)

## New predictions
(0 to 3, in the format above. "No falsifiable prediction from this meeting"
plus why, if that is the case: it is a legitimate outcome.)

## To confirm
(ambiguities, doubtful speakers, open contradictions, questions for the user)

<page url="...">Transcript — 2026-10-07 Gorrand negotiation</page>
```

**The order of the sections is not aesthetic.** `Prediction outcomes` comes first,
before the briefing, because it forces the reckoning **before** the agent writes a
nice coherent story.

### The transcript goes in a SUBPAGE, not in a toggle

A toggle only collapses the UI: reading the page still returns its content. Putting
the transcript in a toggle means that **every reread of that meeting drags the whole
transcript along**.

A subpage, in the parent's markdown, is a single `<page url="...">` tag: reading the
Meeting costs one line instead of ten thousand words. In the UI the difference is
minimal — a link instead of a collapsible toggle.

The subpage is created with a separate call, with the parent set to the ID of the
Meeting page.

### How to split the transcript into blocks

Three limits apply together: 2,000 characters per block, 100 blocks per request,
500 KB per payload.

Prescription: split **at speaker changes**, grouping turns up to ~1,500 characters
per paragraph, and write in several calls of max `blocks_per_notion_request` (80)
blocks.

Splitting at turns rather than at fixed character counts is not aesthetic: the
transcript is there to reread **who said what**, and a turn cut in half between two
blocks is exactly the information you want to keep.

### Note on the language of the Dynamics section

Write "refused three times on price and gave way on the inspection", not "seemed
nervous". The distinction is not one of style: it is the perimeter of
`ethical-legal-limits.md` applied to the writing format.
