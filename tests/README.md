# Test suite

**Entry rule: do not touch a real recording before the four synthetic cases and the
eight negative tests pass in a sandbox.** Real recordings are a scarce, unrepeatable
resource: they are spent measuring quality, not discovering that a property is
missing.

## How to run it

The tests run against a **pair of sandbox databases** — `People TEST` and
`Meetings TEST`, in a Notion page `Sandbox` — with their IDs in a separate copy of
the configuration. **The tests must never touch the real archive.**

The simplest way: make an empty folder, run `setup-notion-memory` there asking for a
**per-project instance** (it creates `./.ghostwriter/` with its own
`configuration.md`), name the databases with the `TEST` suffix, and run the suite from
that folder. Your real `~/.ghostwriter/` is never read while a local `.ghostwriter/`
exists.

Run phrase: `run the test suite in the sandbox`.

In the transcripts `ME` is the user: put a fictional name and alias for yourself in
the sandbox configuration; the agent recognises `ME` from it and does **not** create a
page for them. All names, companies and suppliers are fictional. Each case states the
turn numbers it refers to: the turns are numbered in order, starting from 1, with
`ME`'s turns counted too.

## The cases

| File | What it tests |
|---|---|
| `cases/T1-supplier-change.md` | internal meeting, procedural obstruction: telling a no from a toll |
| `cases/T2-merriwether-quote.md` | client negotiation, disguised objection; **health data of a third party** |
| `cases/T3-partners.md` | family-business confrontation, an economic objection that is not economic |
| `cases/T4-plenary.md` | closes T1's prediction as **REFUTED**: measures the ability to lose |
| `cases/negatives.md` | eight cases where the correct behaviour is to **stop** |

T4 is run **after** T1, on the same sandbox archive: it checks that the agent declares
a prediction refuted instead of rephrasing it.

## What they assess, and what not

The transcripts were written together with the expectations, so they test the
**mechanics, the discipline and the refusals** well, and the quality of insight
poorly. Quality is judged only on real recordings.

**Do not add synthetic cases "to cover more".** Add one each time a new defect is
found, as a regression test, and not before.

## Regression gate for unattended runs

The same four cases are rerun in any unattended environment (a server, a scheduled
agent, a webhook-driven pipeline) before activating any automation, and the output is
compared with the same expectations. That is why the files are plain markdown and the
expectations are checkable lists, not prose.

The transcripts are in English. If you use Ghostwriter in another language, it is
worth translating them and rerunning: the quotes in the expectations must match the
transcript verbatim.
