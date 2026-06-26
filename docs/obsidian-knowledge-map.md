# Obsidian Knowledge Map

This map preserves useful research, tests, and errors from the Obsidian vault
without copying the whole vault into the repo. Use it when a fresh AI session
needs the project memory behind the compact repo libraries.

Vault root:

```text
C:\Users\dariy.n\Documents\Obsidian Vault
```

## High-Value Massing Research

| Topic | Obsidian source | Repo use |
| --- | --- | --- |
| Form operators from Moscow reference imagery | `50 Research\Moscow Massing\Form Operator Library 2026.md` | Basis for `docs/libraries/massing/form-operator-library.md` |
| Decision order for massing generation | `50 Research\Moscow Massing\Massing V2 Decision Library 2026.md` | Basis for `docs/libraries/massing/massing-decision-library.md` |
| Visual typology catalog | `50 Research\Moscow Massing\Massing Typology Catalog 2026.md` | Expand future typology library and case prompts |
| Mayor-ready massing criteria | `50 Research\Moscow Massing\Moscow Mayor Ready Massing 2026.md` | Approval-risk checks: silhouette, fifth facade, TEP hard stop |
| Office massing references | `50 Research\Moscow Massing\Archi.ru Office Massing References 2026.md` | Office-specific variant grammar and risk notes |
| Moscow style trends | `50 Research\Moscow Massing\Property Insider Moscow Style Trends 2026.md` | Context and market-language calibration |
| Channel/image signal research | `50 Research\Moscow Massing\m0n1ch Architecture Channel Massing Signals 2026.md` | Source-language and precedent mining |
| Skyscraper silhouette grammar | `50 Research\Moscow Massing\Materia Skyscraper Silhouette Grammar 2026.md` | Tower crown and skyline rules |
| Moscow dimensional baselines | `50 Research\Moscow Dimensions\Moscow Building Dimensional Library 2026.md` | Basis for `docs/libraries/standards/moscow-building-dimensional-library-2026.md` and generator YAML defaults |

## High-Value Rhino And CAD Lessons

| Topic | Obsidian source | Repo use |
| --- | --- | --- |
| Rhino massing iterations v5-v8 | `30 Projects\AI Geometry Workflows\LLM to CAD Massing\Rhino Test Massing Iterations v5-v8 2026-06-11.md` | Case library: compact podium, separated tower, no random pavilions |
| Rhino pilot massing review | `30 Projects\AI Geometry Workflows\LLM to CAD Massing\Rhino Pilot Massing Review 2026-06-11.md` | Error library: circulation-first, gap checks, red-line discipline |
| Moscow BC rejected variants | `30 Projects\AI Geometry Workflows\LLM to CAD Massing\Moscow BC Massing Error Library 2026-06-16.md` | Already mirrored in `docs/errors/massing/moscow-bc-massing-error-library.md` |
| Site shape and footprint system | `30 Projects\AI Geometry Workflows\LLM to CAD Massing\Site Shape and Footprint Decision System 2026.md` | Expand generic site-planning library |
| BC site-massing typologies | `30 Projects\AI Geometry Workflows\LLM to CAD Massing\Business Center Site-Massing Typologies 2026.md` | Expand business-center typology library |
| Image-to-CAD massing protocol | `50 Research\Architecture Image to CAD Massing 2026-05-05.md` | Reference-modeling protocol: parameter table before geometry |
| Constructive grammar before geometry | `50 Research\Constructive Grammar Before Geometry 2026-05-28.md` | Already promoted into reference-modeling gates |
| Rhino clear model postmortem | `50 Research\Rhino Clear Model 4 Postmortem 2026-05-18.md` | Scenario 2 cleanup case memory |
| Mesh cleanup strategy | `50 Research\Rhino Mesh Cleanup Strategy 2026-05-18.md` | Scenario 2 anti-global-decimation rules |
| Solid reconstruction from messy meshes | `50 Research\Rhino Solid Reconstruction From Messy Meshes 2026-05-18.md` | Scenario 2 reconstruction-by-parts workflow |

## Decisions And Guardrails Worth Keeping Close

| Decision | Obsidian source | Repo use |
| --- | --- | --- |
| Feature-preserving reconstruction path | `40 Decisions\Decision - Feature Preserving Mesh Reconstruction Path.md` | Mirrored by repo decision and error ledger |
| Rhino reference modeling stage gates | `40 Decisions\Decision - Rhino Reference Modeling Stage Gates.md` | Stage-gate policy for Scenario 1 |
| Rhino Aurox release guardrails | `40 Decisions\Decision - Rhino Aurox Modeling Release Guardrails.md` | Tool behavior and validation policy |
| Rhino and Grasshopper area note | `20 Domains\Area - Rhino and Grasshopper.md` | General domain memory |
| GH MCP automation lessons | `30 Projects\Grasshopper Plugins\GH MCP Automation — Spiral Tower + Facade Lamellae.md` | Adopted-slot rules, C# source strategy, Pavilion 80hz lamella-attractor case |
| Rhino modeling workflows roadmap | `30 Projects\Skills and Publishing\Rhino Aurox Modeling\Rhino Modeling Workflows Roadmap 2026-05-18.md` | Future skill/tool roadmap |

## Adjacent Research To Import Later

| Topic | Obsidian source | Why it may matter |
| --- | --- | --- |
| GhCrowdFlow research intake | `30 Projects\Grasshopper Plugins\GhCrowdFlow Crowd\09 - Research Intake.md` | Pedestrian movement validation for Scenario 3B |
| GhCrowdFlow test scenes | `30 Projects\Grasshopper Plugins\GhCrowdFlow Crowd\10 - Test Scenes and Validation Reports.md` | Potential route-width and bottleneck checks |
| GhCrowdFlow integration lessons | `30 Projects\Grasshopper Plugins\GhCrowdFlow Crowd\14 - Integration Lessons 2026-04-23.md` | How to connect movement logic to Rhino/Grasshopper |
| GhCrowdFlow closure | `30 Projects\Grasshopper Plugins\GhCrowdFlow Crowd\15 - Final Crowd Simulation Research Closure 2026-04-27.md` | What not to overbuild in pedestrian simulation |

## Import Backlog

1. Promote the generic site/footprint decision system into
   `docs/libraries/massing/site-planning-pattern-library.md`.
2. Promote the visual typology catalog into
   `docs/libraries/massing/massing-typology-catalog.md`.
3. Add a compact `docs/workflows/rhino-reference/rhino-reference-modeling-protocol.md` from the
   image-to-CAD massing note.
4. Add a Scenario 3B movement validation note from the GhCrowdFlow research,
   but only as lightweight route/bottleneck heuristics first.
5. Keep this map updated whenever a useful Obsidian note is discovered but not
   fully migrated.

## Rule

Use Obsidian as source memory and this repo as portable operating memory.

```text
Obsidian note found
-> apply docs/repo-knowledge-boundary.md
-> extract durable rule / pattern / case / error
-> add compact repo page or index pointer
-> update NEWS.md
```

Only promote notes that are geometry-actionable, reusable, source-aware,
buildable, checkable, shareable, and compact. Keep raw research, private
context, speculative trends, and long precedent catalogs local until distilled.
