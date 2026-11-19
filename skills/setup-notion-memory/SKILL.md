---
name: setup-notion-memory
description: >
  Ghostwriter first-run setup: creates the Ghostwriter home folder with the private
  configuration templates, then creates from scratch the two Notion databases of the
  counterpart memory ("People" and "Meetings") with all the properties, relations,
  rollups and views of the schema, and writes the resulting IDs into the
  configuration. Use it on first install or to repair an incomplete schema, when the
  user says "set up Ghostwriter", "create the databases on Notion", "initialise the
  memory", "I have a new workspace, prepare everything", "the Speaker aliases
  property is missing from People", "check that the schema is complete", or when
  another Ghostwriter skill reports that configuration.md is missing. Do not use it to
  add people or meetings: process-meeting and the other skills do that.
license: MIT
---

# Set up the memory on Notion

Runs **once** in the life of an instance. It refuses to start if `configuration.md`
already contains the Notion IDs, unless the request is explicitly a **repair**: in
that case compare the real schema with `notion-schema.md` and add **only what is
missing**, without touching the rest.

References like `profiling-references:references/<file>.md` resolve to
`../profiling-references/references/<file>.md` relative to this skill's directory;
`profiling-references:<file>` resolves to `../profiling-references/<file>`.

Reply in the user's language. Database names, property names and select options are
created **exactly as in the schema, in English**, whatever the user's language.

## Step 0 — The Ghostwriter home and the private files

Load `profiling-references:references/core-rules.md`.

**Where:** by default `~/.ghostwriter/`. If the user asks for a separate instance for
the current project (for example one for work and one personal), use
`./.ghostwriter/` in the current working directory instead. Never put these files
inside the plugin folder: they would be overwritten on update.

**If `configuration.md` does not exist there yet (first run):**

1. create the home folder, and inside it `transcripts/incoming/` and
   `transcripts/archive/`;
2. copy `profiling-references:configuration.example.md` → `configuration.md`,
   `profiling-references:style.example.md` → `style.md`,
   `profiling-references:deletions.example.md` → `deletions.md`.
   **Copy, never overwrite:** if a target file already exists, leave it alone;
3. tell the user where the files are, and ask them to fill in, at least: `me.name`,
   `me.aliases` (including the misspellings their transcription tool produces),
   `me.contact_email`, `subordinates`, `preferences.time_zone`, and
   `preferences.language` if they do not want `auto`. Explain in two lines why
   `me` and `subordinates` matter: the first keeps them from profiling themselves,
   the second keeps a team member from being treated as a counterparty. `style.md`
   can wait until they first use `compose-message`.

   If the mode is interactive, you may collect these values from the user in the
   conversation and write them into the copied `configuration.md` for them. Never
   invent them.

Do not create anything on Notion until `me.name`, `me.aliases` and
`me.contact_email` are filled in: without them the agent does not know whom to exclude
from profiling and the page disclaimer stays incomplete.

Then load `configuration.md`,
`profiling-references:references/notion-schema.md`,
`profiling-references:references/page-templates.md` and
`profiling-references:references/execution-modes.md`.

## Step 1 — Privacy check

**Mandatory check before creating anything:** list the members of the target Notion
workspace. If it returns anyone besides the user (and bots), **stop**. In a company
workspace an administrator can access the content, and a dossier on colleagues
readable by the company is the worst possible scenario for this system.

## Step 2 — Private container page

Create a page `Ghostwriter` in draft mode, which makes it **private at workspace
level**: it does not ask where to put it, does not share it, does not attach it to an
already-shared page.

**Do not** use an existing page as parent, unless the user confirms that page is not
shared with anyone.

Record its ID as `parent_page_id`.

## Step 3 — People database, without relations and rollups

Create `People` under that page, with all the base properties of `notion-schema.md`
(including `User notes`) **except** the relations and rollups: `Meetings`,
`Processed in`, `Influenced by`, `Influences`, `Last meeting`, `Meeting count`,
`Useful meetings`.

With the Notion MCP connector the schema is passed as `CREATE TABLE` in SQL DDL
dialect, **not** as a properties JSON (see
`profiling-references:references/tools.md` if a tool is not where you expect it).
Respect the names **character for character**.

Record `database_id` and `data_source_id`.

## Step 4 — Meetings database, with the relations to People

Create `Meetings` with all its 11 properties, including **two** relations to People:

```sql
"Participants"        RELATION('<DS_PEOPLE>', DUAL 'Meetings'),
"Profiles processed"  RELATION('<DS_PEOPLE>', DUAL 'Processed in')
```

Each one automatically creates its twin on People (`Meetings` and `Processed in`). This
is how the circular dependencies between the two databases are resolved without
declaring the relations twice.

The two relations are distinct and serve different purposes: `Participants` is *who
was there*, `Profiles processed` is *whom I have already written*. Their difference is
what makes an interrupted processing run repeatable.

Record `database_id` and `data_source_id`.

## Step 5 — The self-relation (the critical point)

The two columns are added to People in **a single call**, each declaring the name and
id of its twin:

```sql
ADD COLUMN "Influenced by" RELATION('<DS_PEOPLE>', DUAL 'Influences' 'influences');
ADD COLUMN "Influences" RELATION('<DS_PEOPLE>', DUAL 'Influenced by' 'influenced_by')
```

**This step may fail, and that is expected.** Two ways, with the remedy:

- **the second `ADD COLUMN` is rejected as a duplicate** (the first already created
  the twin): redo with only the first line, then reread the data source to see what
  the generated twin is called, and if needed rename it to `Influences`.
- **the DDL is rejected entirely:** manual fallback, about 40 seconds in the UI. On
  People → new property → *Relation* → choose **People itself** → enable *"Show on
  People"* → rename the two sides to `Influenced by` and `Influences`.

**Do not go to step 6 before verifying, by rereading the data source, that both
properties exist with the exact names.** The rollups of the next step refer to
properties by name: a relation named differently makes them fail too.

## Step 6 — The rollups

```sql
ADD COLUMN "Last meeting" ROLLUP('Meetings', 'Date', 'latest_date');
ADD COLUMN "Meeting count" ROLLUP('Meetings', 'Date', 'count');
ADD COLUMN "Useful meetings" ROLLUP('Processed in', 'Date', 'count')
```

Note that the three rollups draw from **two different relations**: the first two from
`Meetings` (attendances), the third from `Processed in` (the meetings where there was
evidence). `Profile reliability` is computed on the third: a person who was silent at
ten meetings does not have a reliable profile, and `Meeting count` would say the
opposite.

For counts the function is `count` (counts the related pages) and **not**
`count_values`, which counts the non-empty values of the target property: a meeting
without a date would not be counted. The target property `Date` is mandatory in the
syntax even when the function ignores the value.

**If it fails, do not block the setup.** Rollups are the only elements of the schema
that are entirely **derived**: they contain no information, they compute it. Two
fallbacks:

1. *manual* (preferred): the user creates them in the UI in three clicks each — new
   property → *Rollup* → Relation `Meetings`, Property `Date`, Calculate *Latest date*
   / *Count all*;
2. *degraded*: proceed without them. The agent counts the pages of the `Meetings`
   relation on the fly when reading a profile. Only the recency sort of the `Index`
   view and at-a-glance readability are lost.

In the degraded fallback, write `rollups_available: false` in `configuration.md`.

## Step 7 — Verify

Reread both data sources and compare with this checklist:

- [ ] People has **26** properties (19 base + 4 relations + 3 rollups)
- [ ] Meetings has **11** properties, `Participants` and `Profiles processed` included
- [ ] `People.Meetings` ↔ `Meetings.Participants` and
      `People.Processed in` ↔ `Meetings.Profiles processed` are **two distinct
      bidirectional pairs**, not four one-way relations
- [ ] `Useful meetings` draws from `Processed in`, not from `Meetings`
- [ ] `User notes` exists on People
- [ ] `Influenced by` and `Influences` point to People and are paired with each other
- [ ] **no AI or autofill property** on either database
- [ ] all names match `notion-schema.md` character for character

Then try the full loop: create a Person `ZZ Test`, reread it, move it to the trash. If
this does not work, processing will not work either.

## Step 8 — The two views

| View | On | Configuration |
|---|---|---|
| `Queue` | Meetings | filter `Status != Processed`, sort `Date` ascending, columns: Title, Date, Status, Participants, Error message |
| `Index` | People | sort `Last meeting` descending, columns: Name, Category, Relationship, Organization, Alignment with me, Last meeting, Meeting count, Profile reliability |

No other views.

**If the `!=` operator is not supported in the filter:** use
`FILTER "Status" = "To process"` and add a quick filter on `Status`. Record the
outcome in `environment_notes`.

## Step 9 — Write the configuration

Write into `configuration.md`, section `notion`: `parent_page_id`, the four IDs
(`database_id` **and** `data_source_id` for each database — the API tells them apart
and queries want the second), the URLs of the two views, and `rollups_available`.
Touch nothing else in the file except `environment_notes`.

## Step 10 — Hand over the manual checklist

Print the list of **everything the connector could not create**, with the exact
property name, type and options, so the user can do it by hand.

**Self-relations and rollups are the most likely candidates to fail.** This flow
treats that outcome as normal, not as an error: do not say setup failed if the rest is
in place.

Add the hygiene checklist that concerns the user, not the agent:

- [ ] checked the recording and consent rules that apply in my country
- [ ] checked that company policies do not forbid a personal recorder in meetings
- [ ] Notion workspace on an email address **different** from my work one
- [ ] two-factor authentication on Notion, on the recorder's account and on that email
- [ ] encrypted disk
- [ ] Notion AI **not** used on these two databases
- [ ] `me.aliases` complete, `subordinates` filled in
- [ ] if recording with PLAUD: speakers renamed in the app, voice recognition on
- [ ] test suite (`tests/` in the plugin repository) run against sandbox databases
      before the first real recording
