# Notion schema

Exact names, types and options. Property names must match **character for
character**: queries and writes look them up by name.

Property names and select options are **always in English**, whatever the user's
language: they are the contract between the skills and the databases. Only the
free-text content written into them follows the user's language.

## Database "People"

One page per counterpart. The user does **not** have a page.

| Property | Type | Options / notes |
|---|---|---|
| `Name` | title | |
| `Category` | select | `Work` · `Family` · `Other` |
| `Relationship` | select | `Colleague` · `Direct report` · `Manager` · `Co-owner` · `Client` · `Supplier` · `Partner` · `Family member` · `Friend` · `Other` |
| `Organization` | rich_text | |
| `Role` | rich_text | |
| `Speaker aliases` | rich_text | aliases separated by ` \| `, from most specific to most generic |
| `Key drivers` | multi_select | `Status` · `Security` · `Control` · `Autonomy` · `Recognition` · `Belonging` · `Financial result` |
| `Decision style` | select | `Analytical` · `Intuitive` · `Consensual` · `Directive` · `Avoidant` |
| `Communication style` | rich_text | |
| `Goals and interests` | rich_text | |
| `Fears` | rich_text | topics that need preparation, not weak spots |
| `Sensitive topics` | rich_text | same |
| `Effective levers` | rich_text | 4-line format of `analysis-method.md` §7 |
| `Things to avoid` | rich_text | things that do not work or backfire |
| `Firm positions` | rich_text | |
| `Negotiable positions` | rich_text | |
| `Alignment with me` | select | `Ally` · `Favorable` · `Neutral` · `Skeptical` · `Opponent` |
| `Profile reliability` | select | `Low` · `Medium` · `High` |
| `User notes` | rich_text | **the agent always reads it and never writes it.** See below |
| `Meetings` | relation → Meetings | twin of `Meetings.Participants`, created automatically |
| `Processed in` | relation → Meetings | twin of `Meetings.Profiles processed`: **the idempotency receipt** |
| `Influenced by` | relation → People | self-relation, twin of `Influences` |
| `Influences` | relation → People | self-relation, twin of `Influenced by` |
| `Last meeting` | rollup | on `Meetings` → `Date` → `latest_date` |
| `Meeting count` | rollup | on `Meetings` → `Date` → `count` — attendances, **silent ones included** |
| `Useful meetings` | rollup | on `Processed in` → `Date` → `count` — **this is what feeds reliability** |

**Total: 26 properties** (19 base + 4 relations + 3 rollups).

### `User notes`: your word wins

A field that **you** write and the agent **never touches**. The agent reads it at
every operation and, in case of conflict with what it inferred, **what is written
here prevails**.

It serves two purposes: correcting the system when you know something it cannot see
("he's not skeptical, he had a family problem in March and it's over now"), and being
the rectification procedure if the person asks for their profile to be corrected.

### `Processed in`: the idempotency receipt

A person has been processed for a meeting **if and only if** they appear in
`Meetings.Profiles processed` of that meeting.

A relation is better than a text anchor in the history for three reasons: it **cannot
be destroyed by compaction** of the history; it is structured, so counting useful
meetings becomes a rollup instead of a manual count; and it is checked with a
property read instead of a text search in the page body.

It is still useful to also write the anchor `MTG:<Recording ID>` in the history
entry: it costs 15 characters and keeps the entry readable and traceable outside
Notion.

### Notes that matter

- **`Profile reliability` has short labels** (`Low`/`Medium`/`High`), not
  `Low 1 meeting`. The computation rule lives in `analysis-method.md` §4, not in the
  option name.
- It stays a **select** and not a formula, so the user can lower it by hand when they
  know a profile is unreliable for reasons the agent cannot see.
- **Its computation uses the `Useful meetings` rollup**, not `Meeting count`: the
  latter counts attendances, silent ones included, and a person who was silent at ten
  meetings does not have a reliable profile.
- **Select values are written only if they exist.** Before writing a select, compare
  the value with the literal list in this table, **character for character**. If it
  is not there, write nothing and flag it: an invented value gives no error, it
  silently creates a new option in the database.
- The **selects** `Key drivers`, `Decision style`, `Alignment with me` are filled
  only when the evidence is at `pattern` level. Until then they stay empty.

## Database "Meetings"

One page per recording.

| Property | Type | Options / notes |
|---|---|---|
| `Title` | title | |
| `Date` | date | the date of the meeting, not of processing |
| `Participants` | relation → People | `DUAL 'Meetings'`: creates the twin on People |
| `Category` | select | `Work` · `Family` · `Other` |
| `Type` | select | `Meeting` · `Negotiation` · `1-on-1` · `Phone call` · `Informal` |
| `Status` | select | `To process` · `Speakers to identify` · `Processed` · `Error` |
| `Recording ID` | rich_text | deduplication key, unique, never edit by hand |
| `Recording link` | url | |
| `Profiles processed` | relation → People | `DUAL 'Processed in'`: who has already been written for this meeting |
| `Summary` | rich_text | cap `max_chars_text_property` |
| `Error message` | rich_text | filled only when `Status = Error` |

**Total: 11 properties.**

`Participants` and `Profiles processed` are two different things, and the difference
drives idempotency: *who was there* versus *whom I have already written*. A rerun
processes exactly the difference between the two sets.

`Error message` matters: without it the `Error` status says that something broke but
not what, and recovery becomes guesswork.

### Naming trap

The Notion connector requires properties named exactly `id` or `url` (in any
capitalisation) to be referenced as `userDefined:id` / `userDefined:url`.
`Recording ID` and `Recording link` do not fall into that case: **never rename them**
to `ID` or `URL`.

## What the statuses mean

| Status | Operational meaning |
|---|---|
| `To process` | the page exists and the transcript is safe, but profiles may be half-updated. It is the default after creation. |
| `Speakers to identify` | a human confirmation of who a speaker is is needed. **No profile has been touched.** |
| `Processed` | complete transaction. It is the **last** act of every processing run and works as a commit flag. |
| `Error` | something broke in a way it cannot recover from on its own. `Error message` says what. |

The principle: **the transaction state lives on Notion, not in the agent's
session**. A rerun three days later, on another machine, knows exactly where it left
off.

## Technical API limits that constrain the schema

| Limit | Value | Consequence |
|---|---|---|
| rich_text per block | 2,000 characters | text properties are short snapshots, not archives. Operational cap: 1,800. |
| blocks per request | 100 | the transcript is written in several calls of max 80 blocks |
| payload | 500 KB | a 60-minute meeting (~60 KB) fits |
| related pages per request | 100 | irrelevant at these scales |
| rate limit | about 3 requests/second | a meeting with 6 participants is ~20 calls: it fits, but **no parallelism** |

## Two views, and that's it

| View | On | Configuration | What it is for |
|---|---|---|---|
| `Queue` | Meetings | filter `Status != Processed`, sort `Date` ascending | it is the user's to-do list and the basis of reconciliation |
| `Index` | People | sort `Last meeting` descending | human consultation **and** paged read path for the agent beyond 100 people |

No other views: filters by category or alignment are two clicks when needed, and an
extra view is noise nobody looks at.
