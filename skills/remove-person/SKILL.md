---
name: remove-person
description: >
  Ghostwriter: deletes a person's profile from the counterpart memory on Notion,
  together with their traces in the linked meetings — to honour a GDPR erasure
  request or to clean up a profile created by mistake. Use it when the user says
  "delete X's profile", "remove everything you have on that person", "they asked for
  their data to be deleted", "take that team member out of the database", "I created
  a duplicate person, remove it". It always first lists, item by item, what will be
  deleted and waits for explicit confirmation; in unattended runs it stops and
  reports without deleting anything.
license: MIT
---

# Remove a person

**In autonomous mode this skill refuses to operate** (DP-9): it stops, reports, and
deletes nothing. It is the only skill for which autonomous mode denies the operation
entirely.

References like `profiling-references:references/<file>.md` resolve to
`../profiling-references/references/<file>.md` relative to this skill's directory.

## Step 0 — Configuration

Load `profiling-references:references/core-rules.md`, then `configuration.md` from
the Ghostwriter home (`./.ghostwriter/` if it has one, otherwise `~/.ghostwriter/`),
then `profiling-references:references/notion-queries.md`,
`profiling-references:references/notion-schema.md`,
`profiling-references:references/page-templates.md` and
`profiling-references:references/execution-modes.md`. If `configuration.md` does not
exist: stop and point to `setup-notion-memory`. Reply in the user's language.

## Step 1 — Find the person

Query by name/alias. **If it is ambiguous, do not proceed**: ask which one.

## Step 2 — Impact inventory

Order matters: references are removed **before** the page, otherwise you lose the list
of where to look.

1. Query Meetings with filter `Participants contains <person>` → the complete list of
   meetings to clean.
2. Query People with a filter on `Influenced by` and on `Influences` → who points to
   them in the influence graph.

Present the inventory item by item: how many Meeting pages mention them, which ones,
in which they are the only other participant, how many other People mention them.

## Step 3 — Wait for explicit confirmation

Show the inventory and **stop**. Do not proceed on a generic "yes" to some other
question: a confirmation of this list is required.

## Step 4 — Clean up, in this order

For **each Meeting** in the inventory:

1. remove the person from `Participants` (and from `Profiles processed`);
2. remove their `### <Name>` subsection under `## Briefing`, and every mention of
   their name in `## Dynamics` and `## Recommended move`;
3. **the transcript subpage is deleted, not redacted**, if the person appears in it as
   a speaker. A transcript is the rawest personal data in the archive and cannot be
   reliably cleaned by searching and replacing names;
4. if after the removal the meeting has no profiled participants left, delete the
   whole Meeting page.

For **each other Person** found in step 2:

5. the `Influenced by` / `Influences` relations clean themselves up when the page is
   deleted, because they are relations. **Free-text mentions do not:** search for the
   name in the text properties (`Effective levers`, `Firm positions`, `Goals and
   interests`, …) and in the history entries, and replace it. **This is the step that
   gets forgotten and that lets the data survive the deletion.**

Finally:

6. move the Person page to the trash.

## Step 5 — Say clearly what is left to do by hand

Three things the agent does **not** do, and all three must be stated. Without them, the
procedure **has deleted nothing**: it has only hidden.

- **Empty the Notion trash.** A page in the trash can be recovered, that is, it is not
  deleted. It takes: *Settings → Trash → delete permanently*, for the Person page and
  for the transcripts removed in step 4. The connector does not expose this function,
  and in any case an irreversible deletion must go through the user's hands.
- **Page version history.** This is the gap that is always forgotten. When in step 4
  you replace a name in another page's text, **the previous version stays in that
  page's history** and can be opened and restored. The window depends on the Notion
  plan (days on the free plan, longer on the others). Two consequences to tell the
  user:
  - if the deletion can wait, it is enough to know **by when** the old versions expire,
    and to tell the person concerned;
  - if it must be immediate, the only route that works is to **duplicate the cleaned
    page and delete the original**: the copy is born without history.
- **Clean the local transcripts** in the archive folder of the Ghostwriter home that
  concern that person. Until then the data is deleted from Notion but not from disk.

## Step 6 — Log the deletion

Append to `deletions.md` in the Ghostwriter home (`paths.deletions_log`; if it does
not exist, create it from `profiling-references:deletions.example.md`): date, number of
meetings cleaned, reason (data subject request / error / other).

**Without the person's name.** A deletions log that contains the names of the deleted
defeats the deletions. An opaque identifier and the count are enough.

```markdown
- 2026-10-07 · opaque id: P-7f3a · 4 meetings cleaned, 1 meeting deleted,
  2 transcripts deleted · reason: data subject request · trash emptied: yes
```
