# Ghostwriter

*[Leggi in italiano](README.it.md)*

A Claude Code plugin that keeps an evidence-backed profile of the people you
negotiate with, built from the transcripts of your meetings and stored in your own
Notion workspace.

## The problem

Between one meeting and the next you forget what people actually care about. Who
needs to justify a decision to whom. What the client said about delivery dates three
months ago. Which concession unblocked things last time. Meeting notes don't help:
they record what was decided, not what each person wants, fears, and will accept.

Ghostwriter reads the transcript of a meeting and keeps, for each counterpart, a
profile that grows over time: drivers, decision style, effective levers, things to
avoid, fears, firm and negotiable positions. **Every line is backed by a verbatim quote
with its timestamp.** When there is no quote, the field stays empty. Before the next
meeting, it tells you what each person risks if they say yes, what to ask, and what
not to say. It drafts the follow-up. It never sends anything.

## How it works

```
recording ──► transcript ──► process-meeting ──► Notion: Meeting page + updated profiles
 (PLAUD, or      (text only,                       + briefing, recommended move,
  any recorder)   never audio)                       follow-up draft, predictions

prepare-meeting · compose-message · consult-profile   read the profiles, write nothing
```

1. You record a meeting you took part in (a PLAUD device, a phone, anything).
2. You get a transcript: from PLAUD, from any transcription service, or locally with
   `tools/transcribe.py`.
3. `process-meeting` normalises it into numbered turns, identifies who spoke, extracts
   facts, positions and interests, closes the open predictions, and updates each
   person's profile on Notion — one person at a time, with a quote for every claim.
4. `prepare-meeting`, `compose-message` and `consult-profile` only read.

Two Notion databases hold everything: **People** (one page per counterpart) and
**Meetings** (one page per recording, with the transcript in a subpage). The state
of every processing run lives on Notion, so an interrupted run resumes where it
stopped instead of duplicating.

Every briefing closes the open **predictions** and opens new ones, in falsifiable form
(`IF I do X, THEN they will do Y; REFUTED IF Z`). A profile that cannot be proved wrong
cannot be corrected either. A hit rate under 40% means the profile is wrong; above 90%
means the predictions are too obvious.

## The profile

| Field | What goes in it |
|---|---|
| Key drivers | Status, Security, Control, Autonomy, Recognition, Belonging, Financial result — only once a pattern is seen in 2+ meetings |
| Decision style | Analytical, Intuitive, Consensual, Directive, Avoidant — only after an actual decision was observed |
| Communication style | how they talk, with quotes |
| Goals and interests | what a position lets them do or avoid |
| Fears | risks they perceive, written as topics that need preparation, not weak spots |
| Sensitive topics | business topics to prepare for |
| Effective levers | interest → move → why it works for them → cost to you |
| Things to avoid | what doesn't work or backfires |
| Firm / Negotiable positions | negotiable only if they stated a condition ("if…, then…") |
| Alignment with me | Ally, Favorable, Neutral, Skeptical, Opponent |
| Profile reliability | Low / Medium / High, from the number of meetings with real evidence |
| User notes | yours: the agent reads it, never writes it, and it always wins |

Each claim carries its confidence level (`hypothesis`, `observed`, `pattern`) and the
number of meetings it rests on. Hypotheses never enter the profile fields: they go
into a "to verify" list as open questions. A profile with three fields filled and
eight empty is a healthy profile.

## What it will never do

- **Analyse audio.** No tone, pitch, hesitation, or emotion inferred from the voice.
  Text only. The EU AI Act (art. 5(1)(f)) prohibits inferring emotions from biometric
  data such as voice in the workplace; working only on the text is what keeps the
  system outside that ban.
- **Send anything.** It writes drafts. An automatic send based on a psychological
  profile is exactly what must not be able to happen by mistake.
- **Evaluate the people who report to you.** No performance judgements, no use for
  hiring, promotion, duties or discipline. Using it that way would make it a
  high-risk system under the AI Act (Annex III) and a workplace-monitoring tool under
  most labour laws. People listed as your subordinates get a profile that is mostly
  empty by design, and their words are not archived in full.
- **Write anything without a quote.** An empty field beats plausible psychology.
- **Guess who a speaker is.** If it is not certain, it stops and asks: a wrong
  attribution poisons two profiles for good.
- **Record special-category data** (health, politics, religion, union membership,
  sexual orientation, ethnicity — GDPR art. 9). If it comes up, it is redacted and
  never used.
- **Profile people who were not in the room**, or process recordings of conversations
  you were not part of.
- **Keep data after a deletion request.** `remove-person` cleans the person out of
  every page and tells you the manual steps (trash, version history, local files) that
  a real GDPR erasure needs.

The test behind all of it: every line must be one you could show to the person it is
about. The framing is "what does this person risk if they say yes", not "where do I
push".

## Requirements

- [Claude Code](https://claude.com/claude-code)
- The **Notion MCP connector**, connected to a **personal** Notion workspace (not your
  company's: a workspace admin can read everything in it)
- Optional: a **PLAUD** recorder with its MCP connector, to fetch transcripts directly
- Optional: **mlx-whisper** on an Apple Silicon Mac, to transcribe audio locally with
  `tools/transcribe.py`

## Install

As a plugin:

```
/plugin marketplace add rlfszn/ghostwriter
/plugin install ghostwriter@ghostwriter
```

Or copy the skills by hand (keep all seven folders together: they reference each
other as siblings):

```bash
git clone https://github.com/rlfszn/ghostwriter
cp -r ghostwriter/skills/* ~/.claude/skills/
```

## First run

Say **"set up Ghostwriter"**. The `setup-notion-memory` skill:

1. creates your **Ghostwriter home**, `~/.ghostwriter/`, and copies the templates into
   it: `configuration.md`, `style.md`, `deletions.md`, plus `transcripts/incoming/` and
   `transcripts/archive/`;
2. asks you to fill in `configuration.md` — at minimum `me` (your name, every alias a
   transcript may use for you, a contact email) and `subordinates` (everyone who
   reports to you). `me` keeps you from profiling yourself; `subordinates` keeps a
   team member from being treated as a counterparty;
3. checks that the Notion workspace has no other members, then creates the two
   databases, their relations, rollups and views, and writes the IDs back into
   `configuration.md`.

Your private files live **outside the plugin**, so updates never touch them. For a
separate instance (say, one for work and one personal), run the setup from a project
folder and ask for a per-project instance: it creates `./.ghostwriter/` there, and the
skills use it whenever you work from that folder.

Fill in `style.md` with 3-5 real messages you sent before using `compose-message`,
otherwise the drafts will sound like the agent, not like you.

By default the skills run in **autonomous** mode: they never stop to ask, they leave
anything doubtful marked "to confirm" on Notion. Start a request with
`MODE: interactive` (or put that line in your `CLAUDE.md`) if you want to be asked.
While `confirm_before_writing_profiles` is `true`, interactive runs show you every
profile change before writing it.

## Usage

| You say | Skill | Result |
|---|---|---|
| "process this morning's meeting" | `process-meeting` | Meeting page + updated profiles + briefing |
| "tomorrow I'm seeing Mark about the budget, how do I approach him?" | `prepare-meeting` | goal, what he risks if he says yes, questions, zero-cost concessions |
| "write me the message for Barlow" | `compose-message` | a draft in your register, to reread |
| "what do we know about Farnsworth?" | `consult-profile` | the profile, and how many meetings it rests on |
| "delete X's profile" | `remove-person` | full clean-up for GDPR, after your confirmation |
| "set up Ghostwriter" / "create the databases on Notion" | `setup-notion-memory` | first-run setup, once |

The skills reply, and write on Notion, in your language. Notion property names stay in
English: they are the contract the queries rely on.

### Transcribing locally

`tools/transcribe.py` transcribes audio on your Mac without sending it anywhere:

```bash
uv venv --python 3.11 .venv && uv pip install --python .venv/bin/python mlx-whisper numpy
.venv/bin/python tools/transcribe.py --language en meeting.m4a
```

The output goes to `transcripts/incoming/` in your Ghostwriter home, without speaker
labels: the agent attributes speakers from the content and says so. With PLAUD and the
speakers renamed in its app, this step is not needed.

## Using it with other agents

The skills are plain `SKILL.md` markdown files with standard frontmatter. Any agent
that loads skills in that format can use them; there is no code to integrate, only
text to load. Point the agent at `AGENTS.md` for the always-on rules, give it a Notion
connector, and keep the same Ghostwriter home. The external contract is the Notion
schema (`skills/profiling-references/references/notion-schema.md`): anything that
reads or writes the two databases follows it.

The skills were written to run unattended as well (a webhook from your recorder, a
scheduled job). In that mode they never ask, never overwrite a filled field, never
delete, and `remove-person` refuses to run. See
`skills/profiling-references/references/execution-modes.md`.

## Layout

```
.claude-plugin/              plugin and marketplace manifests
AGENTS.md                    always-on rules, for any agent
skills/
  profiling-references/      LIBRARY: core rules, method, schema, limits, templates
  process-meeting/           the main flow
  prepare-meeting/           read-only
  compose-message/           read-only + drafts
  consult-profile/           read-only
  remove-person/             destructive, asks for confirmation
  setup-notion-memory/       first-run setup
tools/transcribe.py          local transcription with mlx-whisper
tests/                       4 synthetic cases + 8 negative tests
```

One copy of the logic: the analysis method, the Notion schema and the legal limits
live in the library, and the skills point to them.

## Tests

`tests/` holds four synthetic meetings with expected results and eight negative tests
where the right behaviour is to stop (insufficient material, noisy transcript,
unknown speakers, sensitive data, deceptive message, single meeting, HR use, voice
analysis). Run them against sandbox databases before your first real recording: say
"run the test suite in the sandbox". Instructions in `tests/README.md`.

## Legal

This is not legal advice. You are responsible for complying with the laws that apply
to you: in many countries recording a conversation requires telling the other people,
or their consent; workplaces often have policies on recording devices; and data
protection law (the GDPR in the EU) applies to the profiles you keep. Check your
company's policies before recording any meeting — if they forbid it, don't. Tell
people you record, stop when they ask, and if someone asks what you have written about
them, show them the page. `skills/profiling-references/references/ethical-legal-limits.md`
explains the rules the agent applies and the ones that are up to you.

## License and author

MIT. Created by Elia Rolfi.
