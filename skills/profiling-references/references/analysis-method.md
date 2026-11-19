# Analysis method

How a transcript becomes profile updates. The rules here are binding: if a rule and
an output need conflict, the rule wins.

*All names and companies in the examples are fictional. The examples use a small
B2B supplier of warehouse conveyor systems; the method is the same in any business.*

## 0. Non-negotiable principles

1. **Text only.** No access to the audio, no audio URL opened, no inference from
   tone, pitch, pauses, prosody, speech rate.
2. **No claim without a quote.** Every line that ends up in a profile is anchored to
   a verifiable quote. Without a quote, the claim does not exist.
3. **Blind analysis before comparison.** Steps P1–P5 are run *without* having read
   the person's profile properties. The profile is opened only at P6. This stops
   the system from confirming itself.
4. **"I don't know" is a valid and preferred output.** Filling an empty field with
   plausible psychology is the worst possible failure.
5. **Interests, not vulnerabilities.** Reason about what the person wants to obtain
   and what they risk losing. Test: every line must survive being read by the person
   concerned.
6. **No evaluative use on employees.** No judgement of performance, fitness or
   conduct. See `ethical-legal-limits.md`.

## 1. Normalisation (P0)

Before any reasoning, rewrite the transcript as numbered turns with a time anchor:

```
[T1 | 00:12] Speaker 1: Right, let's start from the quote.
[T2 | 00:31] Speaker 2: I don't see that conveyor at that price.
```

The pair `[Tn | mm:ss]` is the **citation anchor** used throughout the system. The
timestamp makes the quote findable even if the numbering changes.

Mark the user's turns with `Me:` (aliases in `configuration.md`). **They never
generate profiling**, but they stay in the analysis of the dynamics: they show who
gives way to whom.

**If the input comes from a PLAUD connector (or any connector that serves
transcripts):** use the transcript block, paging until exhausted. If paging does not
complete, the meeting goes to `Status = Error`: never analyse a truncated
transcript. The tool's own note (summary, action items) is valid **only** as factual
corroboration, and any sentence in it that attributes moods ("the client seemed
interested", "tense tone") is discarded here, before it enters the analysis.

## 2. The reasoning chain

The order is binding. Each step consumes only the output of the previous ones; no
step introduces material that cannot be traced to a turn.

| # | Step | Output | Stop rule |
|---|---|---|---|
| P0 | Normalisation + speaker identification | numbered turns, speakers CERTAIN/PROBABLE/UNKNOWN | a non-marginal speaker not CERTAIN → `Speakers to identify`, stop (§6) |
| P1 | Fact extraction | facts with quotes | no fact without a quote |
| P2 | Conversation map | who proposes, objects, gives way, decides, stays silent | no acoustic inferences |
| P3 | Stated positions | per person: asked / refused / conceded / postponed | only what was said |
| P4 | Underlying interests | per person: why that position serves them | if not deducible, say so |
| P5 | Operational Theory of Mind | ToM block per person | every line quoted or declared not deducible |
| P6 | Formulating inferences | inferences in the contract format (§3) | cap from `configuration.md` |
| P7 | Profile delta | field-by-field proposal (§4) | gate G5 before writing |
| P8 | Writing | updated Notion pages | see `notion-queries.md` |

### P1 — Facts

Only verifiable things: decisions, numbers, dates, amounts, commitments, requests,
documents mentioned, deadlines.

```
[FACT] Quellan quantifies a loss of €8,000 in 2025 on the custom-conveyor model —
"last year we burned 8,000 euros on that model" [T11 | 06:12]
```

### P2 — Conversation map

Rebuilt from the **content and sequence of turns**, never from sound:

- who opens the topic, who makes the proposal, who objects, who rephrases, who closes;
- **who gives way**: a speaker abandons a stated position within the same meeting
  (you need the quote of the initial position *and* of the final one);
- **who blocks**: explicit refusal, or postponement without a date ("let's talk
  about it later", "I'll check with…");
- **who stays silent**: list of attendees with number of turns and the topics they
  did not speak on;
- **visible alliances**: a speaker explicitly supports another's position
  (quote of both turns required).

**Rule on interruptions.** You state that A interrupted B **only** if the text shows
it: a truncated turn with a transcript marker, or explicit content ("sorry, but…",
"let me finish"). Diarisation splits turns even without real interruptions; with no
textual evidence, there is no talk of interruptions.

### P3 — Stated positions

For each CERTAIN person, four lists with quotes: **asked**, **refused**,
**conceded**, **postponed**. Record the context ("in front of the partner", "with
their spouse present"): a concession made in front of others is not equivalent to
one made in private, and the context is part of the claim.

### P4 — Underlying interests

From position to interest. Guiding question: *if this position were obtained, what
would it allow them to do or avoid?* The interest is legitimate by definition
(keeping the margin, not overrunning deadlines, not being contradicted in public, not
doing the same work twice). If the transcript gives no material, write literally
`not deducible from this meeting`.

### P5 — Operational Theory of Mind

Three questions, in order, for each CERTAIN person. Fixed format:

```
### ToM — Victor Quellan (partner)
- What I think he believes about me: that I am willing to sacrifice margin to close
  — "you decide, but…" [T13 | 06:41]  (confidence: hypothesis)
- What he personally risks if he says yes: having to justify the exception to the other partners
  — "I don't want to hear about it at the shareholders' meeting" [T13 | 06:41]  (confidence: observed)
- Whom he has to justify himself to: shareholders' meeting  [T13 | 06:41]
- Zero-cost symbolic concession: a written note with margin and the reason for the
  exception, signed by me, handed to him before the shareholders' meeting
- Real cost to me: 10 minutes of preparation, no financial cost
```

The first three lines require a quote; if there is none, write
`not deducible from this meeting` and close the block there.

The **zero-cost symbolic concession** is valid only if: (a) it answers the risk
identified in line 2, (b) it costs neither money nor contractual commitments, (c) it
would be acceptable if the person knew it had been designed. If any of the three
fails, the line becomes `no zero-cost concession identified`.

### P6 — Formulation and budget

At most `max_new_inferences_per_person` (default 5) **new** inferences per person per
meeting; P1 facts are not subject to the budget. If more emerge, keep the ones with
the strongest evidence and **discard** the others: they do not pile up in a queue.
The budget is the main brake on overproduction of psychology.

### P7 — Delta and gate

Produce the change proposal field by field: current value → proposed value →
reason → quote. Apply gate G5 (§5).

If `preferences.confirm_before_writing_profiles` is `true` **and** the mode is
interactive, show the delta and **wait for confirmation** before touching profile
properties. The Meeting page is created anyway. In autonomous mode the gate does not
apply, but the non-destructive restrictions of `execution-modes.md` do.

## 3. The evidence → inference contract

### Canonical format (internal reasoning and delta proposal)

```yaml
claim: "Accepts longer delivery times if the safety sensors stay in the spec"
field: "Negotiable positions"
person: "Dana Fernwick"
type: position             # fact | position | interest | fear | style | relationship
evidence:
  - anchor: "[T31 | 18:04]"
    quote: "if it's running by September, we'll agree on the rest"
    nature: direct         # direct | behavioural | reported_by_third_party
confidence: observed       # hypothesis | observed | pattern | refuted
context: "with her CEO present"
```

**Where this format is persisted: nowhere.** It is the shape of your reasoning and
of the delta proposal, not a record to archive. What persists is the compact version
below: **the marker `(level · N mtg · last <date>)` is the ledger**, and the history
is its log. If you need to know how many meetings a claim rests on, read it from the
marker; if you need the evidence, follow the meeting link in the history. There is
no second archive to keep in sync, and that is deliberate: two truths diverge within
the second month.

### The three natures of evidence

| Nature | What it means | How far it can go |
|---|---|---|
| **direct** | the person explicitly states the content of the claim | up to `pattern` |
| **behavioural** | **≥2 turns by the same speaker, in the same meeting, that enact the behaviour** described by the claim, each quoted | up to `pattern`, but see below |
| **reported by a third party** | someone else states something about the person | never beyond `hypothesis`, and it counts for the speaker, not the subject |

**Behavioural** evidence exists because the structured fields are behavioural by
nature: nobody says "my driver is Control" or "my decision style is Analytical".
Without this category those fields would stay empty for ever, and the system would
produce only quotes without structure.

But it is weaker than direct evidence, so it has three constraints:

1. **≥2 quoted turns** in the same meeting that enact the behaviour are needed — a
   single turn is `hypothesis`;
2. the claim must **describe the observed behaviour**, not interpret it: "asked to
   review the numbers before deciding, in 2 turns out of 2 decisions" is
   behavioural; "distrusts other people's numbers" is interpretation, and stays
   `hypothesis`;
3. to rise to `pattern` you still need **≥2 distinct meetings**, as with direct
   evidence.

### Compact format in Notion properties

Short lines with the confidence marker at the end:

```
Accepts delivery at 90 days if the safety sensors stay in the spec (observed · 1 mtg · last 2026-03-14)
Wants the line running before peak season (pattern · 3 mtg · last 2026-03-14)
```

### Confidence scale — operational criteria

| Level | Minimum criterion | Where it goes |
|---|---|---|
| **hypothesis** | interpretation of a quote that does not say the thing explicitly; indirect evidence; information reported by third parties | **only** in the page body, section *Contradictions / to verify*, as an open question |
| **observed** | ≥1 **direct and explicit** quote in 1 meeting: the person says the thing, it is not deduced | profile property, marker `(observed · 1 mtg · last <date>)` |
| **pattern** | ≥2 direct quotes in **≥2 distinct meetings on different dates**, consistent, at least one in the last 12 months | profile property, marker `(pattern · N mtg · last <date>)` |
| **refuted** | contrary evidence that passed the reversal rule (§4, case b) | leaves the properties, stays in the history as "superseded on <date>" |

**Non-accumulation rules**

- Two quotes from the **same** meeting do not make a pattern, even if far apart in
  time within the recording.
- A quote **reported by a third party** ("Barlow says Renner will never sign") is
  evidence about **Barlow**, not about Renner. About Renner it is at most
  `hypothesis` and does not enter his properties.
- An inference cannot use another inference as evidence. The evidence→claim chain is
  **one step** long.
- The select fields `Key drivers`, `Decision style`, `Alignment with me` are set
  **only** at `pattern`. Until there is a pattern, they stay empty.

**Zero-evidence rule.** A statement without a quote does not enter the profile, does
not enter the history, does not enter the briefing. If you think it is useful, write
it as a **question** in *Contradictions / to verify*:
"To verify: does Quellan decide alone or always go through the shareholders'
meeting? No direct evidence."

### Where a claim goes: routing table

A claim has **one** destination only. Without this rule the same content ends up in
three different fields depending on how it was phrased, and the profile becomes
redundant and inconsistent.

| `type` | Destination property | Criterion |
|---|---|---|
| `position` | `Firm positions` **or** `Negotiable positions` | negotiable **if and only if** the quote contains a condition ("if…, then…", "provided that"); otherwise firm |
| `interest` | `Goals and interests` | |
| `fear` | `Fears` | the risk perceived by the person. If the topic needs preparation on your side, **also** `Sensitive topics` |
| `style` | `Communication style` (how they talk) **or** `Decision style` (how they decide) | `Decision style` is a select: `pattern` only, and only if **you observed a decision** |
| `relationship` | `Influenced by` / `Influences` | needs the quote of both turns |
| `fact` | **no property** | facts live on the Meeting page, not in the profile |

`Key drivers` is **not** fed directly by a claim: it is derived from ≥2 concordant
claims of type `interest` or `fear`, over ≥2 distinct meetings.

`Effective levers` and `Things to avoid` are not claims but **operational
conclusions**: they are written in the 4-line format of §7 and must rest on claims
already present.

**Related claim** = an existing claim with the same destination **and** the same
object (the same thing being talked about: the price, the timing, the exclusivity).
If there is a related claim, case (a), (b) or (b2) of §4 applies; if not, it is new,
case (c).

## 4. Update rules (the delta)

| Case | Condition | Property | Page body | Confidence |
|---|---|---|---|---|
| **(a) Confirmation** | new quote consistent with an existing claim | **do not rewrite the text**; update only the marker (`N mtg`, `last <date>`) | 1 history entry | `observed` → `pattern` if the threshold is reached |
| **(b) Contradiction** | new quote incompatible with an existing claim | if `observed`: downgrade to `hypothesis`, field → "uncertain position, two opposite findings". If `pattern`: **do not touch the property** | entry in *Contradictions* with **both** quotes and what would be needed to decide | a pattern is reversed only by **2 consistent contrary observations in 2 distinct meetings** |
| **(b2) Declared evolution** | the person says they changed their mind, or the context changed (role, mandate, ownership) | reverse **immediately**, quoting the change | "change of position declared on <date>" + old claim archived | the new claim starts at `observed`, it does not inherit the level |
| **(c) New** | new claim, no related claim | insert at the level the evidence supports; max `max_claims_per_text_property` | 1 history entry | the claim in excess leaves the properties but **survives in the history** |
| **(d) Present but silent** | participant with no turns of relevant content | **no change of any kind** | on the Meeting page: "<Name>: present, no contribution on the topics discussed" | none; **silence does not advance reliability** |

**Asymmetry rule.** A single observation never overwrites a pattern. The pattern is
the system's memory; a single meeting is a sample. The only exception: declared
evolution (b2), where the evidence is the person themselves.

**`Profile reliability`** is computed on **useful meetings**, i.e. those in which
the person produced at least one new piece of evidence or a confirmation. The count
is immediate: **the useful meetings are the history entries**, because an entry is
written only when there was evidence. Do not use the `Meeting count` rollup, which
also counts silent attendances.

- Low: 1 useful meeting
- Medium: 2–4 useful meetings
- High: 5+ useful meetings **and** no open contradiction on `pattern` claims
- With ≥2 open contradictions, reliability is forced to **Medium** even with 10
  meetings

**Decay.** Evaluated **on read**, every time you open a profile. No scheduled
process.

| Field family | Window | On expiry |
|---|---|---|
| `Firm positions`, `Negotiable positions`, `Goals and interests` | 6 months | claim marked `(to re-verify — last <date>)` and downgraded one level |
| `Fears`, `Sensitive topics`, `Effective levers`, `Things to avoid` | 12 months | as above |
| `Key drivers`, `Decision style`, `Communication style`, `Alignment with me` | 24 months | as above |
| any `pattern` no longer observed | 18 months | leaves the properties, stays in the body as "historical pattern (<period>)" |

**Context reset.** If a change of role, company, ownership or mandate emerges,
**immediately** mark as `to re-verify` all claims in `Firm positions`, `Negotiable
positions`, `Goals and interests` and `Alignment with me`, regardless of date. Style
and drivers stay.

## 5. Anti-hallucination guardrails

### G1 — No voice, tone, prosody

No statement about tone, volume, hesitation, pauses, speed, breathing, timbre.
**Vocabulary banned in output:** *tense tone, voice breaking, seemed nervous,
hesitant, faltering, embarrassed, visibly irritated, enthusiastic* (if deduced from
the way of speaking).

On the text too: describe **behaviours and interests**, not emotional states. Not
"he was angry" but "refused the same proposal twice and asked to postpone
[T22 | 11:40]".

Why: see `ethical-legal-limits.md`. The method is compliant *precisely because* it
works on text only; touching the audio would drop that compliance.

### G2 — No special categories (GDPR art. 9)

Do not infer and do not record inferences about health, sex life or sexual
orientation, political opinions, religious or philosophical beliefs, trade-union
membership, racial or ethnic origin, genetic or biometric data. Full procedure in
`ethical-legal-limits.md`.

### G3 — "Said X" vs "I think they think X"

Every line produced carries an explicit marker:

| Marker | Meaning | Requirement |
|---|---|---|
| `[FACT]` | event, number, date, commitment | direct quote |
| `[STATED]` | the person said this about themselves or their position | direct quote, verb of saying |
| `[INFERENCE]` | the agent's reading | quote + confidence level |
| `[REPORTED BY <name>]` | third parties speaking about someone | quote; counts for the speaker, not the subject |

`[FACT]` and `[STATED]` are written in the indicative. `[INFERENCE]` lines **must**
contain an epistemic marker ("probably", "the evidence suggests", "hypothesis:")
**and** the confidence level. Writing an inference with the grammar of a fact is
forbidden.

- **Wrong:** "Quellan does not trust the sales team."
- **Right:** "[INFERENCE · hypothesis] Quellan may not consider the sales
  estimates reliable: he asked twice to review the numbers before deciding — "I'll
  redo these numbers myself" [T18 | 09:50]."

### G4 — Ambiguous or low-quality transcript

**Quality gate.** The transcript is low quality if at least one condition is true
(thresholds in `configuration.md`):

- more than 15% of turns contain illegible or truncated text, or markers of
  incomprehension;
- more than 30% of turns have no speaker label;
- useful speech is under 3 minutes or 20 turns;
- transcript paging did not complete;
- the number of speaker labels exceeds the participants declared by the user.

When quality is low: `Status = Error`, create the Meeting page with only the
transcript and a factual summary, **zero profile updates**, and say which condition
was triggered and what is needed to proceed.

**Local ambiguity** (the sentence lends itself to two readings): **do not choose**.
Write the quote and both readings in *Contradictions / to verify*, and move on.

### G5 — Verification gate before writing

Before writing anything on a Person, check every claim with these seven questions.
**A single negative answer removes the claim** — it does not soften it, it removes
it.

1. Is there a verbatim quote with an anchor `[Tn | mm:ss]`?
2. Does the quote really say what the claim states, or am I extending it?
3. Is the claim about the person I am attributing it to (and not about whoever was
   talking about them)?
4. Does the confidence level respect the criteria of §3?
5. Is the claim free of references to voice, tone, pauses, emotions?
6. Is the claim free of art. 9 special categories?
7. Would the claim hold if the person read this line?

### G6 — Anti-contamination

- A claim observed on a group is not distributed to individuals ("the family wants
  to close right away" does not become "the wife wants to close right away").
- Knowledge of the organisation does not fill a person's profile ("it's a
  purchasing department, so they'll only look at the price" → forbidden).
- Do not import claims from a similar person, a role, a sector, or a meeting the
  person did not attend.

### G7 — Behaviour on "I don't know"

Explicit sentences, and you stop:

- `Insufficient material on <person> for <field>: in this meeting they have 3 turns, all organisational.`
- `not deducible from this meeting`
- `no zero-cost concession identified`

Producing generic unquoted descriptions ("pragmatic, results-oriented person",
"direct communicator") to avoid leaving fields empty is forbidden.

## 6. Unidentified speakers

### Mapping procedure (in order, stops at the first CERTAIN outcome)

0. **Exclusion of the user** — this check runs **before** all the others. The
   speaker matching the aliases in `configuration.md` is the user: mark them `Me:`
   and exclude them from profiling.
1. **Exact speaker alias.** The label matches a value of `Speaker aliases` on a
   Person. Here you read **only** `Name`, `Speaker aliases`, `Role`, `Organization`,
   `Category`: it is a mechanical lookup, not a reading of the profile (the blind
   analysis principle applies).
2. **Self-naming.** The speaker introduces themselves ("I'm Dana Fernwick").
3. **Vocative by others.** Another speaker calls them by name unambiguously, **at
   least twice consistently**, in turns adjacent to theirs.
4. **Role and content.** They say things only that person can say (speaks for the
   workshop, signs the quote, cites their own delegation). Valid **only as
   corroboration** of points 2–3, never on its own.
5. **Participation consistency.** The person was expected at that meeting. Also
   corroboration only.

### Levels

| Level | Condition | Effect |
|---|---|---|
| **CERTAIN** | exact alias, **or** self-naming, **or** consistent vocative ≥2 times | the profile may be updated |
| **PROBABLE** | no name in the text, but role + content + expected presence converge | **no write to the profile** |
| **UNKNOWN** | no convergence | no write |

### Stop rule

If at least one **non-marginal** speaker is not CERTAIN, the meeting goes to
`Status = Speakers to identify`. *Non-marginal* = has more than 10% of turns **or**
speaks on a decision, a number or a commitment.

In this state: create the full Meeting page (transcript in a subpage, factual
summary, dynamics described with the `Speaker N` labels), **do not touch any
profile**, and write an identification request block for each doubtful speaker:

```
**Speaker 3** — 14 turns (18% of speech). Speaks on: delivery times, workshop load.
Distinctive quotes:
  - "next week I already have three conveyors on the line" [T27 | 14:02]
  - "I don't sign off the commissioning without the data sheet" [T39 | 21:15]
Candidates: 1) Neil Farrowby (installation lead) — talks about workshop load and commissioning;
            2) unknown outsider.
Confirmation needed. I am not adding an alias: "Speaker 3" is not a stable identifier.
```

**Note on the example above:** the confirmation is about *who is in this
recording*, not about adding an alias. `Speaker aliases` accepts **only stable labels
specific to the person** — real name, surname, recurring nickname. Diarisation labels
are assigned **per recording**: today's `Speaker 3` is not tomorrow's `Speaker 3`,
and putting it among the aliases guarantees attributing to Farrowby the words of
whoever takes that position in the next meeting.

After the user replies, **start again from P1** on that speaker's turns: do not
reuse an analysis done on an uncertain identity.

If all doubtful speakers are **marginal**, proceed on the CERTAIN people and note on
the Meeting page that N marginal speakers are unidentified. Their turns are used
**only as interactional context** ("answered a question about timing"), never to
attribute content or positions to anyone.

### Anti-pollution rules

- **Never** create a new person on your own initiative to make things add up.
- **Never** merge two speaker labels into one person because "they say similar
  things".
- If the same label seems to carry two identities (incompatible self-references),
  split it into `Speaker 2a` / `Speaker 2b` and mark both UNKNOWN.
- An alias is never added automatically: `Speaker aliases` is changed only on the
  user's confirmation, because a wrong alias pollutes **all** future meetings.
- When in doubt between two real people, **do not pick the more likely one**: stop.

## 7. How to write an "effective lever"

A lever is the description of a **legitimate interest** and of the move that
satisfies it. It is not the description of a weakness and of how to exploit it.

**Prescribed format** for every entry of `Effective levers`:

```
Interest: <what the person wants to obtain or avoid, with quote>
Move: <what I do, concretely>
Why it works for them: <which risk it removes>
Cost to me: <financial / time / none>
```

**The four-question test.** A lever is written only if all four answers are yes:

1. **Disclosure** — if the person read this line, would they find it correct (even
   if uncomfortable)?
2. **Legitimacy** — is the interest one the person would openly claim?
3. **Reversibility** — would I accept the same move being used on me?
4. **Symmetry** — does the move work because it solves a real problem, not because
   it exploits an asymmetry of information, power or personal circumstance?

The same test applies to `Fears` and `Sensitive topics`, which are written as
**topics that need preparation**, not as weak spots. `Things to avoid` lists things
that **do not work or backfire**, not "buttons to press with care".

### WRONG / RIGHT examples

*Names are fictional.*

**1) Partner (Victor Quellan, 30% partner)**

- **WRONG:** "Fears being contradicted at the shareholders' meeting: make him
  understand the exception will be brought to the meeting if he keeps blocking."
  *Why:* uses the fear as a threat; works only through pressure; would not survive
  disclosure.
- **RIGHT:** "Interest: being able to show the shareholders' meeting a number that
  holds — "I don't want to hear about it at the shareholders' meeting"
  [T13 | 06:41]. Move: before every price exception, hand him a written note signed
  by me with margin and reason. Why it works: it removes the risk of having to defend
  a choice that is not his. Cost to me: 10 minutes, no financial cost."

**2) Client in negotiation (Dana Fernwick, operations director at a distributor)**

- **WRONG:** "She mentioned her father's illness and is emotionally stretched:
  insisting on the scenario where peak season fails without the new line will speed
  up the signature."
  *Why:* exploits a personal circumstance and a health datum, builds pressure on a
  fear, violates G2 and the disclosure test.
- **RIGHT:** "Interest: having the line running before peak season — "it has to be
  running by September" [T9 | 04:20]. Move: delivery date written into the contract
  with a penalty, a single named contact with a phone number, two progress dates
  already set in the offer. Why it works: it turns a non-negotiable deadline for her
  into a verifiable commitment. Cost to me: none, the contact person is already
  planned."

**3) Internal lead (Neil Farrowby, installation)**

- **WRONG:** "Can't say no when rushed in front of others: bring him the urgent
  items in the plenary meeting."
  *Why:* designs the move around a personal difficulty and uses the audience as a
  lever; it is also a use of the profile against a colleague.
- **RIGHT:** "Interest: not committing to dates he then cannot keep — "I don't sign
  off the commissioning without the data sheet" [T39 | 21:15]. Move: arrive with the
  week's workload already checked and the data sheet ready, and ask for the date at
  that point. Why it works: it gives him the conditions to say yes without exposing
  himself. Cost to me: 10 minutes of preparation."

**Vocabulary.** Forbidden: *exploit, leverage (a person), push, weak spot,
vulnerability, insecurity, manipulate, corner, play on.*
Required: *interest, perceived risk, condition for saying yes, guarantee,
verifiable, zero-cost concession, what removes the problem for them.*

## 8. Rule on drafts

Generated messages **never quote the profile**, never mention the existence of the
system, and contain no wording the user would not say out loud. A draft that "works"
only because it exploits information the counterpart does not know they gave is not
sent: it is rewritten.

## 9. Predictions: how a profile is made falsifiable

This is what separates a useful profile from a horoscope. A profile that produces no
refutable statements can be neither validated nor corrected: it stays plausible for
ever, and therefore useless.

The mechanism: every processing run **closes** the open predictions on the
participants and **opens** new ones. Predictions live in the `## Open predictions`
section of the Person page; the format is in `page-templates.md`.

### The six requirements of an acceptable prediction

Check them **before** writing it. If one is missing, rewrite it or give up.

1. **Conditional** on a move by the user or on a dated event. Without a condition
   nothing can be tested.
2. **Observable behaviour** in a future transcript or a verifiable external fact:
   asks for a postponement, brings a third party to the meeting, replies within 24
   hours, does not reply, asks for a discount above 5%, signs, changes the subject
   when timing comes up. **Never internal states** ("will be suspicious", "will feel
   under pressure").
3. **Refutable by a written outcome**: the `REFUTED IF` line must exist. If you
   cannot write it, the prediction is void by construction.
4. **Dated**: explicit deadline. Default: 60 days, or the next meeting with that
   person, whichever comes first.
5. **Not generic**: if, swapping the name, the sentence stays plausible for at least
   3 other people already profiled, it is a horoscope. Do the swap and **declare that
   you did** in one line.
6. **Not obvious**: it must not follow from the role ("the purchasing manager will
   ask for the best price"). If the user would have bet 90% on it, it measures
   nothing.

**Forbidden:** "will be cautious"; "won't be enthusiastic"; "might object"; "will
consider carefully"; "will react well if you involve him"; "will keep defending his
department".

**How many:** 1 to 3 per meeting, at most 2 per person. If no acceptable prediction
can be derived, write `No falsifiable prediction from this meeting` plus why
(typically: no future commitment and no pending decision in the material). **It is a
legitimate outcome, not an error:** inventing a prediction to fill the section is the
defect to avoid.

### How the loop is closed

1. At the start of every processing run, **before** writing any analysis, read
   `## Open predictions` of every participant.
2. For each, look in the new transcript for evidence for or against, and assign an
   outcome **with a quote**.
3. The briefing **opens** with `## Prediction outcomes`.
4. Allowed outcomes:
   - **CONFIRMED** — condition met, behaviour observed;
   - **REFUTED** — condition met, behaviour not observed or opposite;
   - **PARTIAL** — condition met, behaviour partly observed (specify what yes and
     what no);
   - **LAPSED** — the condition did not occur before the deadline. Leaves the
     statistics, stays as a note in the history.
5. **No retrofitting.** The text of a prediction is **never modified** after being
   written, and is not rephrased after the fact ("after all I said he wanted
   guarantees") to pass a refutation off as a confirmation. This is the defect that
   makes the whole mechanism useless. If a prediction is refuted, it is declared
   refuted.
6. Every **REFUTED** requires: an entry in *Contradictions / to verify*, a proposed
   revision of the profile, and the application of the two-evidence rule (§4,
   case b). In the briefing the line starts with
   `WARNING: the profile was wrong about …`.
7. **Manual closing.** The user may close a prediction without a new meeting
   ("close P-2026-10-07-01 as confirmed: he signed on 2026-11-12"). Move it to the
   history with source "user's statement".

### How to read the hit rate

```
rate = (CONFIRMED + 0.5 × PARTIAL) / (CONFIRMED + REFUTED + PARTIAL)
```

**Not computed under 3 closed outcomes** per person; under 10 total outcomes read it
as a hint, not a measure.

| Rate | Reading | What to do |
|---|---|---|
| < 40% | the profile is **wrong**, not just incomplete | set `Profile reliability` to Low and **rewrite the extended analysis starting from the meetings' quotes**, not from the previous summary |
| 40–90% | useful zone: the profile informs, it does not decide | carry on |
| > 90% on ≥5 outcomes | **suspicious**: the predictions are obvious or generic | raise specificity (requirements 5 and 6) and flag it in the briefing |

**A very high rate is not a success:** it is the symptom that you have learnt to bet
on safe things.

### The anti-anchoring rule

Evidence is extracted from the new transcript **before** opening the existing profile
(principle §0.3), and only then compared. In the briefing include a collapsible
`Raw evidence extracted` block that **precedes** the comparison.

It is a weak guarantee — the order of the output does not prove the order of the
reasoning — but it makes the defect visible: if the raw evidence already contains the
old profile's vocabulary, anchoring happened.

## 10. What was deliberately excluded

| Excluded | Why |
|---|---|
| Acoustic, prosodic, emotional analysis of audio | legal constraint and the biggest risk; useless for the use cases |
| Personality scores (Big Five, DISC, MBTI, 0–100 scores) | not falsifiable from a transcript, give an illusion of precision |
| Predictive probabilities ("78% will close by April") | invented numbers, cannot be anchored to evidence |
| Network metrics beyond `Influences` / `Influenced by` | what matters is who listens to whom, not centrality in a graph |
| Indices of "manipulability", "resistance", "optimal pressure" | incompatible with the chosen framing |
| Aggregate dashboards and rankings of people | would turn the system into personnel evaluation |
| Emotional summaries from the transcription tool's note | discarded at P0 |
