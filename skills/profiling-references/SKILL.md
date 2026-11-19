---
name: profiling-references
description: >
  Internal library of the Ghostwriter profiling system. Holds the shared logic — core
  rules, analysis method, Notion schema, page templates, query recipes, ethical and
  legal limits, execution modes — plus the templates for the user's private
  configuration. It is never triggered by a user request and produces no output: the
  other Ghostwriter skills (process-meeting, prepare-meeting, compose-message,
  consult-profile, remove-person, setup-notion-memory) read its files when they need
  them. If you are about to read or write Notion for Ghostwriter, start from the
  user's configuration.md in the Ghostwriter home (see references/core-rules.md).
disable-model-invocation: true
license: MIT
---

# Reference library

This skill has no flow. It is where the shared logic lives, read on demand by the
operational skills. **Do not load a reference "just in case":** every file costs
context, and loading one that is not needed is the most common waste in this
system.

## The user's private files (outside the plugin)

| File | Contains | Read |
|---|---|---|
| `<home>/configuration.md` | identity, Notion IDs, paths, preferences, limits | **always, as the first step of every skill** |
| `<home>/style.md` | real samples of the user's messages and their register constraints | only by `compose-message`, before writing |

`<home>` is the Ghostwriter home: `./.ghostwriter/` in the current working directory
if it contains `configuration.md`, otherwise `~/.ghostwriter/`. Details in
`references/core-rules.md`.

These are **instance files, never part of the plugin**: the plugin ships only the
templates `configuration.example.md`, `style.example.md` and `deletions.example.md`
in this folder. If `configuration.md` does not exist, the skill stops and points the
user to `setup-notion-memory`, which copies the templates — it does not infer the
configuration and does not create it on its own.

## The library files, and when they are read

| File | Contains | Read |
|---|---|---|
| `references/core-rules.md` | the inviolable rules, the Ghostwriter home, reference resolution, the language rule | **always, at step 0** |
| `references/execution-modes.md` | interactive vs autonomous, decision points DP-0…DP-9 | at step 0, together with the configuration |
| `references/analysis-method.md` | steps P0–P8, the evidence→inference contract, the guardrails | only when actually analysing a text or reasoning about a profile |
| `references/notion-schema.md` | exact property names, types, select options | before creating or writing properties |
| `references/page-templates.md` | body structure of Person and Meeting pages, with the anchors | before creating or rewriting a page body |
| `references/notion-queries.md` | read and write recipes, filters, limits, what is forbidden to ask | before the first Notion operation of the session |
| `references/ethical-legal-limits.md` | AI Act, GDPR, labour law: what is never written, what is refused | before writing a Person page and before composing a message |
| `references/tools.md` | capability → tool name map, per harness | **only** if a tool is not found under the expected name |

## Who loads what

| Reference | process | prepare | compose | consult | remove | setup |
|---|---|---|---|---|---|---|
| `configuration.md` | yes | yes | yes | yes | yes | yes |
| `core-rules.md` | yes | yes | yes | yes | yes | yes |
| `style.md` | — | — | yes | — | — | — |
| `execution-modes.md` | yes | yes | yes | — | yes | yes |
| `notion-schema.md` | yes | — | — | — | yes | yes |
| `notion-queries.md` | yes | yes | yes | yes | yes | yes |
| `analysis-method.md` | yes | yes | yes | — | — | — |
| `page-templates.md` | yes | — | — | — | yes | yes |
| `ethical-legal-limits.md` | yes | yes | yes | — | yes | — |

## Who may write to `configuration.md`

Only two skills, and only on specific fields:

- `setup-notion-memory` → creates the file from the template on first run (and, in
  interactive mode, fills in the values the user dictates), then writes only the
  `notion:` section and the `environment_notes` flags.
- `process-meeting` → only `environment_notes`, to record what it discovered about
  the environment (e.g. that a markdown construct is not supported).

Everything else is edited by the user by hand.
