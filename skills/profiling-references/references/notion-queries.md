# Notion operations

Read and write recipes. IDs **always** come from `configuration.md`: they are not
written here and are never inferred. *(Names in the examples are fictional.)*

## The reading principle

> **The properties are the profile. The page body is the reasoning.**

To prepare a meeting or write a message you need the profile, not the reasoning. So
the default read is **properties only**, with a filtered query, **without reading
page bodies**.

The page body is read only in three cases:

1. the user asks *why* the agent thinks something;
2. you need to write to the history (and check what is already there);
3. you need to check the *Contradictions* section.

A query on 5 participants returns ~5 × 600 tokens of properties. Five full page
reads would return 20–30 times as much. It is the difference between a briefing that
fits in a conversation and one that does not.

## Finding a person from their aliases

One call per speaker. Row mode (`rows`), **never SQL**: SQL mode consumes a workspace
quota on non-Business/Enterprise plans.

```json
{
  "mode": "rows",
  "data_source_url": "<People data_source_id, from configuration>",
  "filter": {
    "type": "group", "operator": "or",
    "filters": [
      { "type": "property", "property": "Speaker aliases", "propertyType": "text",
        "operator": "string_contains", "value": { "type": "exact", "value": "Gorrand" } },
      { "type": "property", "property": "Name", "propertyType": "title",
        "operator": "string_contains", "value": { "type": "exact", "value": "Gorrand" } }
    ]
  },
  "limit": 10
}
```

Search token: the **surname** if present, otherwise the first name.

### Mandatory convention for `Speaker aliases`

Aliases separated by ` | `, from most specific to most generic:

```
Mark Gorrand | Gorrand | the surveyor | Mark G.
```

Two hard rules:

- **Never add generic diarisation labels** (`Speaker 1`, `Participant 3`) as aliases.
  Speaker numbering is **per recording**: Tuesday's `Speaker 2` is not Thursday's
  `Speaker 2`. Such an alias identifies nobody and guarantees polluting the wrong
  profile.
- **Never a bare first name** if the archive contains more than one person with that
  name. `Mark` alone catches both Mark Gorrand and Mark Vellacott.

### What to do with the result

| Result | Action |
|---|---|
| 1 match | proceed |
| 0 matches | **do not create the person on your own initiative.** See DP-3 in `execution-modes.md` |
| 2+ matches | **do not pick the most likely one.** See DP-2 |

A wrong attribution is the worst damage this system can do: it writes into
Vellacott's profile things said by Gorrand, and from that moment every briefing on
both is false. Better to stop than to guess.

## The deduplication check

**First step of every processing run**, before reading the transcript:

```json
{
  "mode": "rows",
  "data_source_url": "<Meetings data_source_id>",
  "filter": {
    "type": "property", "property": "Recording ID", "propertyType": "text",
    "operator": "string_is", "value": { "type": "exact", "value": "<RECORDING_ID>" }
  },
  "limit": 2
}
```

`string_is` and not `string_contains`: an ID that is a prefix of another would
produce a false positive. `limit: 2` because two results are already a diagnosis.

| Outcome | Action |
|---|---|
| 0 results | new processing |
| 1, `Status = Processed` | **stop.** Point to the existing meeting without rewriting anything. In interactive mode you may offer to reprocess (rewrites the body, does not recreate the page). |
| 1, `To process` / `Error` / `Speakers to identify` | **resume**, not a new processing: reuse the existing page |
| 2 results | anomaly. `Status = Error` on both, `Error message` = "duplicate Recording ID", report it and **do not** write to profiles. |

### How the Recording ID is determined

| Origin | Key |
|---|---|
| PLAUD connector | `plaud:<id of the file returned by the connector>` |
| file named `YYYY-MM-DD_<plaudid>_<title>.txt` | `plaud:<plaudid>` |
| file without a convention, or pasted text | `manual:<first 8 hex digits of the text's SHA-256>` |

For the hash **run a command**, do not compute it in your head:

```bash
printf '%s' "<the text>" | shasum -a 256 | cut -c1-8
```

A model cannot produce a hash reliably, and a wrong hash is worse than no hash: it
creates a duplicate that looks like a new meeting. If you cannot run commands, use
`manual:<YYYY-MM-DD>-<first 40 letters of the first turn, lowercase, no spaces>` and
**declare** that you used the fallback key.

The key is based on content and not on the date, so the same transcript pasted twice
does not create two pages. A meeting without a deduplication key is a meeting that
sooner or later will be processed twice.

## What is read, case by case

| Use case | Calls | What is read |
|---|---|---|
| Pre-meeting preparation | 1 query per participant | properties only |
| Post-meeting briefing | 1 query + 1 page read per participant | properties, plus the body to reread *Contradictions* and append the history |
| Consultation | 1 query, then the page only if the user digs deeper | properties first, body on request |
| Message draft | 1 query per recipient | only `Key drivers`, `Fears`, `Effective levers`, `Things to avoid`, `Firm positions`, `Negotiable positions`, `Communication style` |
| Rereading a past meeting | 1 read of the Meeting | briefing and dynamics. The transcript is in a subpage and is **not** pulled down |

## Context budget, before the analysis

Binding rules when retrieving existing context:

1. The participants' **properties** already arrived with the speaker-resolution
   query. **Do not make a second call** for them.
2. Retrieve the **page body** of participants only, at most
   `max_profile_bodies_loaded` (5), in order of number of turns.
3. **Do not retrieve the pages of past Meetings. Ever.** The history inside the
   Person page *is* the compressed record: that is exactly why it exists. If someone's
   history is too thin to make sense of, the remedy is to improve **how it is
   written**, not to read ten old meetings.
4. People linked via `Influenced by` / `Influences` are retrieved **only as names**
   (already present in the relation), without opening their pages, unless they are
   participants.

**Forbidden:** any unfiltered query on People or Meetings; any generic workspace
search when you already know the data source.

Overall cap on context loaded before the analysis: ~8,000 tokens. If you exceed it,
cut from the bottom of the list of page bodies.

## Beyond 100 people

Row mode has a maximum `limit` of 100 and **no pagination cursor**. To read the whole
archive (e.g. "whom did I see least this year") use view mode on the `Index` view,
paging with the cursor: it has no plan quota. For everything else, row mode.

## Writing: text properties

Updating a property **replaces** the value. There is no append on properties. So:

> Rewrite the whole field, but only after reading the current value and merging it
> with the new one. **Never write a text property without having read it in the same
> run.**

The current value arrives **for free** from the speaker-resolution query: no extra
read is needed. The merge is a summary, not a concatenation: the field is a concise
snapshot of the present, not a log.

Example. `Fears` before:

```
That regional exclusivity gets eroded. That delivery slips past the tender deadline.
```

A new fear emerges from the meeting and one of the two turns out to be over. After:

```
That regional exclusivity gets eroded (recurring, 3 mtg). That the safety
inspection needs a second pass and delays go-live. [Resolved: delivery times,
after the confirmation of 2026-09-30.]
```

The resolved fear **is not deleted**: it is marked as resolved. It helps in future
briefings ("don't reopen the timing topic, it's closed") and it keeps the agent from
believing, six months from now, that it has discovered something new.

### Hard rules

- Cap `max_chars_text_property` (1,800). When exceeded, **summarise**, do not
  truncate: a field cut mid-sentence is worse than a shorter one.
- A property is emptied **only at the user's explicit request**. Never deletion by
  silent subtraction.
- `Key drivers` is updated only with evidence over **at least two distinct
  meetings**. A driver inferred from a single sentence is noise.

## Writing: appending to the history

Appending at the end of the page does not require knowing the existing content: it is
a single call. It works because the history is the **last** section of the page (see
`page-templates.md`).

The check on who has already been written is done **beforehand**, on the meeting's
`Profiles processed` relation (see *The per-person receipt*), not by searching for the
anchor in the page body.

## The write order

This order removes half of the possible inconsistent states by construction:

1. **Create the Meeting page** with `Recording ID`, `Date`, `Title`,
   `Status = To process`. Empty body.
2. Write the Meeting body and the `Summary`.
3. **For each participant**, in sequence: properties → history entry →
   `Profile reliability` → **add the person to `Profiles processed`**.
4. Link `Participants`, set the final `Category` and `Type`.
5. Create the transcript **subpage**, **last**.
6. **Reread the Meeting page and verify** that it has: body with its sections,
   `Summary`, `Participants`, complete `Profiles processed`, subpage. If the check
   fails → `Status = Error` with the detail of what is missing.
7. **Only now** `Status = Processed`, and clear `Error message`.

**Why the subpage goes last.** The tag that inserts it into the parent's body moves
pages, not just references: creating it first means keeping it in the middle of all
the body rewrites that follow, multiplying the chances of moving or losing it. Last,
the body is already settled.

The transcript is safe anyway: it is in the source file in the transcripts folder,
which is not moved to the archive before step 7.

The Meeting page works as a **write-ahead log**: the `Recording ID` is recorded
before any change to profiles, so an interruption can never lose the deduplication,
and `Status ≠ Processed` always and only means "profiles may be half-updated". There
is no state in which profiles were touched without the Meeting page existing.

**Never in parallel.** Two concurrent writes to the same profile overwrite each
other, and the rate limit is about 3 requests per second.

## The per-person receipt

> A person has been processed for this meeting **if and only if** they appear in that
> meeting's `Profiles processed`.

It is a **relation**, not text, and that is deliberate: history compaction rewrites
the page body, and a text receipt would sooner or later be destroyed by the very
mechanism that keeps pages small. A relation is not compacted, is read together with
the other properties, and is counted by a rollup.

The check on rerun is therefore: read the meeting's `Participants` and `Profiles
processed`, and **process exactly the difference between the two sets**.

The relation is added **right after** writing that person's profile, one person at a
time. An honest gap remains: an interruption between writing the properties (or
appending the history entry) and adding the relation leaves the profile updated
without a receipt, and the resume will merge it a second time. Since the merge is a
summary and not a concatenation, the result is **redundant but not corrupt**. It is
not worth a transactional machine to close it.

## Reconciliation

Run it when the user asks, and at the start of every new processing run (it costs one
call).

1. Query the `Queue` view: all Meetings with `Status ≠ Processed`.
2. Diagnosis from the status:
   - `Speakers to identify` → show the unresolved speakers and **wait**. No automatic
     writes.
   - `To process` or `Error` → resume.
3. Read the Meeting page: check that body and transcript subpage exist; if missing,
   redo them.
4. For each participant, check the receipt and, if absent, process.
5. `Status = Processed`, `Error message` cleared.

### Error handling

On any failure: `Status = Error` and `Error message` filled in an **actionable** way —
what was being done, on whom, and the literal error:

```
2026-10-07 14:22 · failed to update properties of Mark Gorrand
(validation_error: content length 2140 exceeds limit of 2000 on "Goals and interests").
Profiles already processed: Vellacott. To redo: Gorrand, Bertram.
```

**Do not retry automatically more than once** on the same error. A blind retry on a
validation error repeats the error; on a rate limit (429) one pause only, respecting
the `Retry-After` header.

### Two anomalies to recognise

| Anomaly | Recognition | Repair |
|---|---|---|
| History entry pointing to a deleted Meeting | the reference does not resolve | **do not delete the entry**: mark it `[meeting no longer available]`. The claim in the profile stays but loses its evidence, and this must be shown, not hidden. |
| Person among the `Participants` of a `Processed` Meeting with no receipt | cross-check | `Participants` was edited by hand after processing. Flag it and ask whether to process that person for that meeting. |
