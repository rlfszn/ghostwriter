# Capability → tool map

**Load this file only if a tool is not found under the name you expected.**
On the normal path it is not needed: the skills describe operations by intent, and
the environment exposes the tools that perform them.

This is the only file in the system where tool names appear. Keeping them here is
what makes the skills runnable from different environments without rewriting them.
Tool names change between connector versions: if a name below does not exist, look
for the tool that performs the same capability.

## Notion

| Capability | Claude Code (Notion MCP connector) | Notes |
|---|---|---|
| create a database | `notion-create-database` | the schema is passed as `CREATE TABLE` in SQL DDL dialect, **not** as a properties JSON |
| add properties to a database | `notion-update-data-source` | `statements` with `ADD COLUMN` |
| create a view | `notion-create-view` | `configure` uses its own DSL |
| create pages | `notion-create-pages` | `creation_mode: "draft"` creates a page that is **private at workspace level** |
| query a database | `notion-query-data-sources` | `mode: "rows"` by default; `"view"` to page; `"sql"` **consumes plan quota** |
| read a page | `notion-fetch` | returns **also** the content of toggles: a toggle does not reduce the cost |
| update properties | `notion-update-page` | `command: "update_properties"`; **replaces**, does not append |
| append content | `notion-update-page` | `command: "insert_content"` with `position: {"type": "end"}` |
| replace targeted content | `notion-update-page` | `command: "update_content"` with `old_str`; requires knowing the exact string |
| trash a page | `notion-update-page` | `in_trash`. It is **not** permanent deletion |
| list workspace members | `notion-get-users` | used by the setup privacy check |

**Not exposed by the connector:** emptying the trash. Permanent deletion is done by
the user by hand from Settings → Trash. That is fine: an irreversible deletion is not
left to automation.

### Mapping to the public API

Useful if one day the same operations have to be done over HTTP instead of through
the connector. Every operation of the system can be expressed with the public API — no
step depends on a capability exclusive to the connector:

| Operation | Endpoint |
|---|---|
| create / update databases | `PATCH /v1/databases` |
| append blocks | `PATCH /v1/blocks/{id}/children` |
| update properties | `PATCH /v1/pages/{id}` |
| query | `POST /v1/data_sources/{id}/query` |

The only operational difference: conversion from markdown to Notion blocks, which the
connector does itself, must be done in code via the API.

## PLAUD (optional)

If you record with a PLAUD device and have a PLAUD MCP connector installed:

| Capability | PLAUD MCP | Notes |
|---|---|---|
| list recordings | `list_files` | filterable by date or keyword |
| get the transcript | `get_transcript` | timestamps and speaker labels; **paged**: follow the cursor until exhausted |
| get the note | `get_note` | summary, action items, topics. Usable **only** as factual corroboration |
| file metadata | `get_file` | also returns an expiring audio link |

> **`get_file`: do not call it to get the audio, and never follow the audio link.**
> The system analyses text only, and this is where compliance is won or lost. If you
> need the title or the date, take them from `get_note` or `list_files`.

The connector has no trigger: it is read-only. Processing is started by the user or
by an external event.

Any other transcription source works the same way: what the skills need is the
transcript text with timestamps and, ideally, speaker labels.

## Verified and not verified

**Verified** (October 2026, Notion MCP connector): the Notion tool names and their main
parameters; the Notion API limits (2,000 characters per rich text, 100 blocks per
request, 500 KB per payload, about 3 requests per second); the behaviour of
`creation_mode: "draft"`; the fact that `notion-fetch` returns toggle contents; the
two-step flow for self-relations; the PLAUD MCP tool names.

**To verify at first real use:**

- whether `notion-create-database` can create self-relations and rollups via DDL;
- whether `string_contains` is case-insensitive;
- whether the `!=` operator is supported in a view filter;
- the exact syntax accepted for the transcript subpage;
- whether speaker labels renamed in the PLAUD app arrive with the real name in the
  transcript returned by the connector.

Each of these has a declared fallback in the skill that meets it. Record the result in
`environment_notes` of `configuration.md`, so the check is done only once.
