# Experience Capture Format

This document defines how a modeling session becomes reusable repository
knowledge. It exists so successful and failed cases can be broken into patterns,
errors, prompts, metrics, and decisions in a consistent shape.

The goal is not to store a transcript. The goal is to make the next AI faster,
less random, and easier to audit.

## Capture Levels

| Level | Purpose | Location |
| --- | --- | --- |
| Case note | What happened in one run | `docs/cases/<case-id>.md` |
| Case index | One-line discoverability | `docs/case-library.md` |
| Pattern/operator | Reusable design or geometry move | `docs/libraries/*.md` |
| Error/anti-pattern | Failure that must not repeat | `docs/error-ledger.md` or `docs/errors/*.md` |
| Metric/default | Numeric design or generator assumption | `docs/libraries/*dimensional*.md` or `.yaml` |
| Prompt/hint | Reusable instruction to an AI or image/model generator | `card-prompts.json` or relevant `docs/libraries/*.md` |
| Decision | Accepted policy/tradeoff | `decisions/YYYY-MM-DD-*.md` |
| Tool note | Backend or automation behavior | `docs/tools/*.md` |
| Changelog | Optional audit note after actionable docs are updated | `NEWS.md` |

## Case Note Template

Use this shape for every durable case in `docs/cases/`.

The `AI Extraction Summary` block is mandatory and must stay near the top of
the file. It is the token-saving layer: a fresh AI should decide whether the
case is relevant from this block before reading the detailed notes.

```markdown
# Case Title

Date:

Status: accepted | medium-success | failed | source-correction | tooling

Scenario: 1 | 2 | 3A | 3B | 3C | 3D | tooling

Case family: rhino-geometry | grasshopper | analysis-cleanup | source-research

## AI Extraction Summary

```yaml
case_family:
use_when:
source_authority:
geometry_grammar:
effective_rhino_gh_route:
key_parameters:
promoted_rules:
failure_gates:
validation:
read_more_when:
related_scripts:
```

Source authority:

- Text:
- Plan/top:
- Elevation/facade:
- Rhino scene/layers:
- User feedback:

Goal:

Input state:

- Files:
- Rhino slot/document:
- Existing layers/variants:
- Units:

What worked:

What failed:

Promoted patterns:

| Pattern | Destination | Action |
| --- | --- | --- |
|  | `docs/libraries/...` | add/update |

Promoted errors:

| Error | Destination | Gate |
| --- | --- | --- |
|  | `docs/errors/...` |  |

Promoted metrics/defaults:

| Metric | Value | Destination |
| --- | --- | --- |
|  |  | `docs/libraries/...` |

Reusable prompt / agent hint:

```text

```

Validation:

- Numeric:
- Visual:
- Source-derived:
- RhinoMCP/tooling:

Links:

- Scripts:
- Captures/artifacts:
- Related cases:
- Decisions:
```

## Promotion Checklist

At the end of a meaningful session, make a small routing table:

| Lesson | Type | Destination | Done |
| --- | --- | --- | --- |
|  | pattern | `docs/libraries/...` | no |
|  | error | `docs/errors/...` | no |
|  | metric | `docs/libraries/<domain>/<topic>.yaml` | no |
|  | case index | `docs/case-library.md` | no |
|  | decision | `decisions/...` | no |

Do not promote everything. Promote only rules that change future behavior.

## Pattern Entry Shape

Use this for design and geometry moves in `docs/libraries/`.

```markdown
## Pattern Name

Use when:

Inputs needed:

Geometry / planning logic:

Parameters:

Acceptance gates:

Failure modes:

Related cases:
```

## Error Entry Shape

Use this for repeated failures in error libraries.

```markdown
## CODE - Error Title

Symptom:

Cause:

Detection:

Correction:

Required gate:

Related cases:
```

## Metric Entry Shape

Use this for dimensional or generator defaults.

```yaml
metric_id:
  value:
  unit:
  scope:
  use_when:
  source:
  warning_flags:
  related_cases:
```

## Prompt / Hint Entry Shape

Use this when a repeatable instruction helps an AI choose the right route.

```yaml
id:
task:
use_when:
read_first:
instruction:
avoid:
related_libraries:
related_cases:
```

Image-generation prompts may stay in `card-prompts.json`. Agent workflow prompts
belong in the relevant library or scenario file, not in a hidden chat.

## Artifact Hygiene

Generated `.3dm`, captures, screenshots, JSON reports, and failed local attempts
should not sit in active docs.

Use:

```text
.tmp_cases/<case-id>/       disposable local work
cases/<case-id>/            promoted shareable case package
archive/<topic>/            historical snapshots
docs/cases/<case-id>.md     compact durable lesson
```

Only promote artifacts when another AI needs them to reproduce or validate the
workflow. Otherwise promote the rule, not the file.
