# Configuration

Single source of truth for identity, Notion IDs, paths and preferences. No other
file in the system contains these values, and no skill infers them.

**Where this file lives:** in the Ghostwriter home — `~/.ghostwriter/configuration.md`
by default, or `./.ghostwriter/configuration.md` in a project folder for a separate
instance. Never inside the plugin folder: it is overwritten on update and it is not
yours to publish.

**To fill in before first use:** every field marked `FILL IN`.
The Notion IDs are written by `setup-notion-memory` on first setup.

```yaml
me:
  name: "FILL IN"                   # first and last name as they appear in transcripts
  aliases:                          # every way your transcription tool may label you
    - "FILL IN"
  role: "FILL IN"
  company: "FILL IN"
  sector: "FILL IN"
  contact_email: "FILL IN"          # goes in the disclaimer: whom to contact to request access

# Who reports to you, directly or indirectly. Determines regime S
# (strongly restricted profiling) in ethical-legal-limits.md §1.
# "Colleague" in the Notion schema does not say who is under whom: this list does.
subordinates: []

# People who asked not to be recorded. The agent processes nothing about them,
# and stops if they appear as speakers.
excluded: []

notion:
  parent_page_id: null              # private container page "Ghostwriter"
  people:
    database_id: null
    data_source_id: null            # format collection://...
  meetings:
    database_id: null
    data_source_id: null
  views:
    queue: null                     # URL of the "Queue" view on Meetings
    index: null                     # URL of the "Index" view on People
  rollups_available: null           # true/false, written by setup

paths:                              # relative to the Ghostwriter home
  transcripts_incoming: "transcripts/incoming"
  transcripts_archive: "transcripts/archive"
  deletions_log: "deletions.md"

preferences:
  time_zone: "FILL IN"              # IANA name, e.g. "Europe/London"
  language: "auto"                  # "auto" = the language you write in; or e.g. "en", "it"
  person_summary_lines: 5
  chat_recap_lines: 15
  draft_tone: "direct, polite, no beating about the bush"

  # During validation keep this true: the agent shows the proposed delta and waits
  # for an ok before touching profile properties. The Meeting page is created
  # anyway. Set it to false when you trust the method.
  confirm_before_writing_profiles: true

limits:
  max_profile_bodies_loaded: 5
  max_chars_text_property: 1800      # margin below Notion's 2000 limit
  max_chars_history_entry: 600
  max_new_inferences_per_person: 5
  max_claims_per_text_property: 3
  history_entries_in_full: 15
  entries_to_compact: 5
  long_transcript_threshold_chars: 120000
  blocks_per_notion_request: 80      # margin below the limit of 100

quality_gate:
  # Heuristic thresholds, to be tuned on the first 10 real meetings.
  max_percent_illegible_turns: 15
  max_percent_turns_without_speaker: 30
  min_useful_turns: 20
  min_minutes_of_speech: 3

environment_notes:
  # Filled in by process-meeting / setup-notion-memory when they discover
  # something about the environment.
  transcript_subpage_works: null
  string_contains_case_insensitive: null
  not_equal_filter_supported: null
```

## Why some values are what they are

- **`confirm_before_writing_profiles: true`** is the gate that makes the validation
  phase safe: if the method produces wrong analyses, you notice before they end up
  in memory. In autonomous mode the gate does not exist, but the non-destructive
  restrictions of `execution-modes.md` apply instead.
- **`max_chars_text_property: 1800`** and not 2000: Notion's limit per rich-text
  block is 2000 characters, and exceeding it is a validation error, not a
  truncation.
- **`me.aliases`** is how the agent recognises you and **excludes** you from
  profiling. If it is incomplete, you risk finding yourself profiled in your own
  archive. Add the misspellings your transcription tool produces for your name.
- **`subordinates`** is the most important list in this file after `me`. Anyone in
  it falls under regime S: most profile fields stay empty and cannot be filled, and
  the agent produces no strategies about them. If the list is incomplete, the system
  treats one of your reports as a counterparty — exactly the mistake you do not want
  to make.
- **`max_new_inferences_per_person: 5`** is a deliberate brake on overproduction of
  psychology, not a technical limit.
- **`language`** sets the language of replies and of free-text Notion content.
  Property names and select options in Notion stay in English whatever you choose.
