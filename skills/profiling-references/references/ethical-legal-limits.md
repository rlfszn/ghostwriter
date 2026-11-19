# Ethical and legal limits

What is never written, what is refused, and the four regimes that change the
perimeter depending on who the person is.

This file is not a disclaimer: it contains operational rules the agent applies
before every write.

> **This is not legal advice.** The references below are to EU law (AI Act, GDPR)
> and, as a worked example of national labour law, to Italian law, where the system
> was first designed. Your country will have its own rules on recording
> conversations and on monitoring workers; check them. If the system leaves personal
> use — if your company sees it, if it enters a company process, if it becomes a
> product — you need real advice. See §6.

## 1. The four regimes

The perimeter of what may be written **depends on who the person is**. A client can
stand up and leave; someone who reports to you cannot: they must come to the meeting
and have no power to renegotiate the relationship. It is this asymmetry, before any
law, that makes a subordinate's profile qualitatively different.

The regime is derived from `Category` and `Relationship`, plus the `subordinates`
key in `configuration.md` — because `Colleague` does not say who is under whom.

| Regime | When | Profile fields allowed | Outputs allowed |
|---|---|---|---|
| **C — Counterparty** | `Category = Work` and `Relationship ∈ {Client, Supplier, Partner}` | all, minus the bans of §2 | all: briefing, preparation, strategies, drafts |
| **P — Peer or superior** | `Relationship ∈ {Colleague, Manager, Co-owner}` and name **not** in `subordinates` | all minus the bans of §2; `Sensitive topics` limited to business topics, reader test applied strictly | briefing, preparation, consultation, drafts. **No** internal positioning strategies |
| **S — Subordinate** | name in `subordinates`, **or** `Relationship = Direct report` | **only** `Communication style`, `Goals and interests` (stated), `Firm positions`, `Negotiable positions`. **Empty and not fillable:** `Key drivers`, `Decision style`, `Fears`, `Sensitive topics`, `Effective levers`, `Things to avoid`, `Alignment with me` | **only** a factual summary of what was decided and what remained open, and drafts of operational messages. **No** behavioural history, **no** strategies, **no** analysis of dynamics that treats them as the object |
| **F — Family** | `Category = Family` | as P, limited to what concerns **their role in the business** | as P |

The regime is **written plainly in the disclaimer at the top of the Person page**,
so that you and the agent reread it at every consultation and it cannot be got wrong
at the next step.

### If the regime cannot be determined: deny by default

If the combination of `Category` and `Relationship` is not one of those in the
table, **or if either field is empty**, the regime is `?` and the permissions of
**regime S** apply, the most restrictive — plus a line in `## To confirm`: "regime
not determined for <name>: fill in Category and Relationship".

This really happens, and early: a person created at the first meeting has
`Relationship = Other` until you correct it. Without this rule the agent would treat
as a counterparty someone it knows nothing about — the opposite of what you want
when nothing is known.

S is not applied **silently**: the line in `To confirm` is mandatory, because a
wrong regime left in place blocks fields that should be filled, and you notice only
if someone tells you.

### Example, regime S

Team meeting, with Tess (a member of your team) present.

- **ALLOWED:** "Prefers to receive priorities in writing at the start of the week;
  in meetings always asks for the delivery date before committing."
- **FORBIDDEN:** "Avoids commitments until she has a date; insecure, needs to be
  cornered."

The first is an observable fact that helps you work better together. The second is
an evaluation of a subordinate's behaviour, and a sentence you could not defend if
Tess read it.

### Mixed meetings: the transcript is not archived in full

If **at least one participant is in regime S** (or regime `?`), the full transcript
is **not** archived in the subpage. A redacted version goes there instead, in which
that person's turns are replaced by a placeholder:

```
[T14 | 07:22] Tess Ombry: [turn not archived — regime S]
```

The briefing can still report what was decided and what remained open, because that
is the organisational content of the meeting.

The reason is practical, not formal: the transcript is the rawest data in the
archive, and archiving a subordinate's words in full means building exactly the
record of what they say in meetings that regime S exists to avoid. The blocked
profile fields would be pointless if the full minutes stayed right next to them.

### Two bans specific to regimes S and F

- **In regime S, 1-on-1 conversations with evaluative or managerial content are not
  processed**: evaluations, reprimands, discussions about duties, grade, pay, leave,
  time off, performance. The agent refuses and suggests taking notes by hand.
  Ordinary work meetings remain processable.
- **In regime F, no pages are created for family members who have no role in the
  business.** The `Family` perimeter is "family members involved in the business",
  not "my family".

## 2. Absolute bans, in every regime

### No inferences from audio, voice, tone

No statement about tone, volume, hesitation, pauses, speed, breathing, timbre. The
audio is not opened, no audio URL is followed, no audio is passed to any model.

**Why it matters:** art. 5(1)(f) of the EU AI Act (Regulation (EU) 2024/1689),
applicable since 2 February 2025, prohibits AI systems that infer the emotions of a
natural person in the workplace, and the ban is tied to inference from **biometric
data** — voice, face, posture. The Commission's guidelines on prohibited practices
(February 2025) clarify that inferring emotions from **written text** is not based
on biometric data and stays outside the ban.

So: working on text only, the method **stays outside the art. 5(1)(f) ban**, because
it does not touch biometric data. Touching the audio signal would bring it back in.
This is not a stylistic precaution, it is the perimeter.

**But that ban is not the only gate**, and passing it does not mean everything else
is fine. At least two more things matter, treated below: that the system does not
slide into the high-risk uses of Annex III (evaluation and management of workers),
and that the data processing holds up under the GDPR. This system's compliance rests
on all the rules in this file together, not on a single article.

Corollaries: sentences in the transcription tool's note that attribute moods are
discarded before analysis; and on the text too, you describe **behaviours and
interests**, not emotional states.

### No special categories (GDPR art. 9 and art. 10)

Do not infer and do not record anything about: health, sex life or sexual
orientation, political opinions, religious or philosophical beliefs, trade-union
membership, racial or ethnic origin, genetic or biometric data, criminal
convictions.

If they come up spontaneously in the conversation:

1. **no claim, no property, no history entry** — never, in any form, not even as a
   hypothesis;
2. in the archived transcript the passage is **redacted** and replaced with
   `[omitted — GDPR art. 9 special category]`;
3. on the Meeting page you note only that an omission occurred, **without saying
   what it was about**;
4. no inference may use that passage as a premise, not even indirectly.

**A case that recurs in some sectors.** When the health condition of the client or
of a family member is **the very object of the supply** (an accessibility
adaptation, a medical aid, a subsidised application), the health datum is treated
**only** as a technical-commercial requirement — type of adaptation, measurements,
certification, paperwork — and lives on the **Meeting** page or in the company CRM,
**not** in the psychological-negotiation profile.

Using it as the premise of an inference about character or negotiability is
forbidden: "her son has a disability, so the mother is fragile and will give in" is
exactly what this system must not produce.

For colleagues and people on your team no health data is recorded, **not even
operational** (absences, appointments, treatments): it is redacted.

### The high-risk boundary

Annex III, point 4 of the AI Act classifies as **high-risk** systems used in
employment to: make decisions on working conditions, promotion or termination;
allocate tasks based on behaviour or personal traits; **monitor and evaluate the
performance and behaviour** of workers.

Where this system sits: **personal support for preparing your own conversations.**
It decides nothing, allocates no tasks, evaluates no one, and its output goes to one
person only.

What would make it slide into high risk — with entirely different obligations
(conformity assessment, technical documentation, human oversight, registration):

| If this happens | The system becomes |
|---|---|
| profiles of people on your team are used to decide duties, workloads, promotions | high-risk, Annex III 4(a) or 4(b) |
| the agent produces recurring evaluations of how people work | high-risk, monitoring and evaluation |
| the output is shared with whoever decides on personnel | high-risk, and the controller becomes the company |
| the system is used in hiring or evaluation interviews | high-risk |

The rules below exist to keep the system on the right side of this line. They are
not caution: they are what avoids ending up with obligations a personal archive
cannot meet.

### No evaluations of workers

Profiles contain no judgements of performance, fitness, conduct or
professionalism, and are not used for decisions on hiring, pay, grade, duties,
promotion, disciplinary measures or termination.

**Why it matters — a national example.** In Italy, art. 4 of the Workers' Statute
(Law 300/1970, as rewritten by Legislative Decree 151/2015) puts conditions on tools
that allow remote monitoring of workers' activity, and requires adequate notice for
the data to be usable in the employment relationship. Art. 8 forbids the employer
from investigating political, religious or union opinions and **facts not relevant
to assessing professional aptitude**. Most jurisdictions have comparable rules on
workplace monitoring; check yours.

Rules like these address the employer. If the user is not the employer, formally
they may not apply — but respect them anyway, for three concrete reasons:

1. **The employer / non-employer boundary is thin.** With a managerial role, a
   delegation, or if the owners know about the system, the processing may be
   attributed to the company: at that moment a remote-monitoring tool exists with no
   agreement and no notice.
2. **They state what a legal system considers off-limits about a worker**, and they
   will be used as a reasonableness yardstick even where they do not apply directly.
3. **The asymmetry is real**, and does not depend on the law.

### No profiling of people who were not present

People **mentioned by others** in a meeting do not get a Person page and are not
profiled. What Barlow says about Renner is evidence about **Barlow**.

### No processing of other people's recordings

Only recordings of conversations the user **took part in** are processed, whoever
provided them.

## 3. The pre-write check

**The last step of every skill that writes to Notion.** Before writing, verify and
declare in the output that you verified:

1. No inference from audio, tone, prosody or paralinguistic annotation.
2. No GDPR art. 9 or art. 10 data in any field.
3. The regime (C/P/S/F) has been determined and is written in the page disclaimer;
   the fields forbidden for that regime are empty.
4. Every statement has its quote and the reference to the meeting.
5. Every sentence passes the reader test (§4).
6. No output resembles an evaluation of a worker.

If a check fails, **do not write**: say which check failed and propose the
rewording.

## 4. The reader test

> Every sentence must be written as if the person were going to read it.

It is not softening: the defensible version contains the **same useful
information**, said in a way that holds.

| Do not write | Write |
|---|---|
| "Fears confrontation with his partner: use this to get him to decide alone." | "Does not make commitments in front of his partner; if a decision is needed, ask for it at a separate moment." |
| "He's in financial trouble and in a hurry to close: hold firm on price." | "Asked twice about payment terms: a deferral is worth more to him than a discount." |
| "Weak spot: wants to be seen as the expert. Flatter him." | "Publicly acknowledging his technical expertise unblocks the discussion; the zero-cost concession is citing him as the reference in the meeting." |

The third pair shows the difference that matters: same information, same practical
use, different defensibility.

## 5. What the agent refuses

Closed list. The agent refuses, says why in **one line**, and proposes the lawful
alternative.

1. **Deceptive messages**: false urgency, fake scarcity, invented deadlines,
   consent never given ("as agreed" when it was not), non-existent third parties,
   false facts.
2. **Exploiting a personal difficulty** that emerged in a transcript: illness,
   disability, separation, bereavement, financial problems, a child's difficulties.
3. **Evaluations of workers** for HR, disciplinary, promotion, duties, termination
   decisions.
4. **Emotion analysis from audio**, tone, prosody, or processing the audio file
   instead of the transcript.
5. **Inferring or recording** political, religious or union opinions, sexual
   orientation, ethnic origin, health status, criminal convictions.
6. **Profiling people who were not present.**
7. **Processing recordings** of conversations the user did not take part in.
8. **Impersonating**: writing a message that appears to come from someone other
   than the user.
9. **Strategies to isolate, discredit or neutralise** a person in the organisation.
10. **Rankings and comparisons** between people, in particular between members of
    your team.
11. **Numeric scores** of personality, reliability or manipulability, and
    psychometric typologies (Big Five, DISC, MBTI, enneagram).
12. **Sharing, exporting or circulating** a profile to third parties, company
    channels, email, chat, presentations.
13. **Low-confidence strategies**: with `Profile reliability = Low` only factual
    observations and verification questions are produced, not strategies.

**Refusal format:** *"I won't do that: [one-line reason]. I can instead
[concrete alternative]."*

Example: *"I won't write a message saying the offer expires on Friday if it isn't
true: it's deceptive and you couldn't defend it. I can write one saying what
concretely changes after Friday — the production slot, the supplier's price list —
if that is true."*

## 6. Things that concern you, not the agent

These are not rules the agent applies: they are conditions that must hold for the
system to be defensible. Check them once, at setup.

- **Recording laws.** Whether you may record a conversation, and whether you must
  tell or get consent from the other people, depends on your country (and sometimes
  on the state or region). Know the rule that applies to you before the first
  recording.
- **Company policies.** Check the code of conduct, IT policy, privacy policy,
  contract and any company regulations to make sure a personal recorder in meetings
  is not forbidden. **If it is forbidden, the project stops here:** no technical
  safeguard cures a policy violation.
- **Say it out loud.** Once per person, not at every meeting:
  - internal: "I record meetings to reread my notes, it stays only on my phone. If
    you'd rather I didn't, I'll turn it off."
  - client or supplier: "So I don't miss the technical details I record the meeting:
    it's only for me, to prepare the proposal."
  If someone says no, **turn it off**, and put their name in the `excluded` key of
  `configuration.md`: the agent processes nothing about them.
- **The right of access is real.** If a person asks what is written about them, the
  answer is to show them the page. This is the practical reason why the reader test
  is not a moral exercise.
- **Access hygiene.** A personal Notion workspace on an email address **different**
  from your work one, so it can never appear in the same sidebar; two-factor
  authentication on Notion, on your recorder's account and on that email; encrypted
  disk; never opened on a company device; fixed rule "screen shared = Notion closed".
- **Do not use Notion AI** on these databases (Q&A, summaries, autofill, AI blocks,
  agents). On non-Enterprise plans model providers may retain data for a period
  before deletion: sending a dossier about a colleague to a subprocessor achieves
  nothing, the agent already does the analysis.
- **You really need legal advice if:** the system becomes known to your company or
  enters a company process; you use it for decisions about someone's employment; you
  want to sell it or have others use it; someone formally exercises their rights and
  you don't know how to respond.

## 7. Risks with no legal remedy

Two are worth knowing because no rule solves them.

**The self-fulfilling profile.** Mark is labelled "Skeptical"; you stop asking for
his opinion in meetings; he feels left out and really starts opposing your
proposals. The profile you wrote has made itself come true. It is the most likely
risk of all. Mitigations, already built into the method: every briefing must contain
the line "what in this meeting contradicts the current profile", and if there is
nothing it says so explicitly, so the question is asked every time; you write
behaviours in context, not traits ("in 3 budget meetings he asked for postponements",
not "he's an avoider"); no scores, no typologies; unconfirmed inferences decay.

**The wrong profile you act on.** Two meetings in which Mark objects to nothing
because he was having a terrible day; the profile says "gives way under pressure";
you go into the annual negotiation without preparing concessions and lose it.
Mitigations: with `Reliability = Low` the agent produces no strategies, only the
questions to ask to verify; the *Contradictions / to verify* section cannot stay
empty after the second meeting.
