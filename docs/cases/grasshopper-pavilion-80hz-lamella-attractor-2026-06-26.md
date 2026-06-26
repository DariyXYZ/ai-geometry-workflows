# Grasshopper Pavilion 80hz Lamella Attractor 2026-06-26

Status: `medium-success / tooling`.

Scenario: build a parametric Grasshopper definition for a Pavilion 80hz-like
small pavilion with lamellas and staggered tilted shingles.

## AI Extraction Summary

```yaml
case_family: grasshopper
use_when: "parametric pavilion, lamella screen, staggered shingles, attractor-shaped facade/skin logic"
source_authority: "user reference images and user-corrected construction sequence"
geometry_grammar: "attractor envelope points -> vertical/slightly curved lamellas -> row-parity checkerboard anchors -> tangent tilted shingles -> continuous top beam"
effective_rhino_gh_route: "repo-stored Rhino 8 C# Script body pasted manually into GH; automate only proven-safe surrounding sliders/groups"
key_parameters:
  units: mm
  width_mm: 5200
  height_mm: 5100
  lamella_count: 13
  rows: 18
  shingle_width_mm: 260
  shingle_height_mm: 430
  shingle_tilt_deg: 15
promoted_rules:
  - "generate checkerboard anchors from row parity and lamella index"
  - "output guides separately from production meshes"
  - "store C# source in repo before GH automation"
  - "use manual paste or a proven bridge for script source"
failure_gates:
  - "do not call SourceCodeChanged(None) on legacy C# Script components"
  - "do not trust reflection/internal GH source setters without same-version smoke test"
  - "avoid overlapping duplicate shingles and half-height-only panel placement"
validation: "small lamella/row count solve first; inspect separate LamellaCurves, LamellaMeshes, AnchorPoints, ShingleMeshes, TopBeamMesh, Log"
read_more_when: "building GH C# pavilion logic or debugging Rhino 8 C# Script source injection"
related_scripts:
  - "scripts/grasshopper/examples/pavilion_80hz_lamella_attractor_csharp.cs"
  - "scripts/grasshopper/examples/pavilion_80hz_lamella_attractor_csharp.md"
```

Source / file:

- User reference images and markup from the 2026-06-24 to 2026-06-26 session.
- Script body:
  `scripts/grasshopper/examples/pavilion_80hz_lamella_attractor_csharp.cs`.
- Concept note:
  `scripts/grasshopper/examples/pavilion_80hz_lamella_attractor_csharp.md`.

## Goal

Create a controllable Grasshopper system:

```text
attractor-driven envelope points
-> vertical / slightly curved generatrix lamellas
-> checkerboard anchor points on odd/even lamellas by row
-> structural lamella thickness centered on each guide line
-> tilted shingle plates tangent to the source lamella
-> continuous top beam tying both sides together
```

## What Worked

- The user-defined construction sequence is the right abstraction. It avoids the
  earlier list/tree errors where duplicate panels overlapped and only half the
  height received shingles.
- Checkerboard placement must be generated from row parity and lamella index:
  row 1 uses lamellas `1, 3, 5...`, row 2 uses `2, 4, 6...`, then repeats.
- The shingle module should be taller along the lamella tangent than it is wide
  through Y. The earlier wide horizontal plates read incorrectly.
- A single C# Script generator is the fastest way to express the logic while the
  form is still being designed. Native nodes are useful for simple chains, but
  this case needs loops, row parity, tangent frames, and geometric validation.
- The C# script should output guides separately from production geometry:
  `LamellaCurves`, `LamellaMeshes`, `AnchorPoints`, `ShingleMeshes`,
  `TopBeamMesh`, `GuideCurves`, and `Log`.

## What Failed

- Programmatic source injection into the legacy `C# Script` component failed.
  Calling `SourceCodeChanged(None)` on
  `ScriptComponents.Component_CSNET_Script` crashed Rhino 8.30 with an
  asynchronous UI-thread `NullReferenceException`.
- The crash happened after the component and sliders were being assembled, so
  the `.gh` definition was not saved.
- `try/catch` around `SourceCodeChanged(None)` is not enough because the
  exception is thrown later through the dispatcher.

## Promoted Rules

- Do not call `SourceCodeChanged(None)` on legacy C# Script components.
- Do not use reflection/internal source setters for production GH definitions
  unless the exact route has passed a disposable smoke test in the same Rhino
  version.
- Treat C# script source as a repo artifact first. Paste manually or use a
  proven source bridge only after the algorithm is stable.
- For user-started/adopted RhinoMCP slots, use `run_python` for capability scan
  and GH document inspection. Avoid `g1_*` probes and avoid leading with
  `run_csharp`.
- When a GH automation attempt crashes Rhino, preserve the script body and
  promote the crash signature into the error library before continuing.

## Reusable Workflow

```text
1. User opens Rhino + Grasshopper and runs MCPStart.
2. Codex runs list_slots + run_python capability scan.
3. If a script component is needed, write/pick a repo-stored paste-ready C# file.
4. User creates a fresh Rhino 8 C# Script component and pastes the code.
5. Codex may automate only proven-safe surrounding graph pieces:
   sliders, standard components, groups, annotations, and validation outputs.
6. Solve small counts first, then increase lamellas/rows.
7. Save the .gh file only after the graph solves without red components.
```

## Pavilion Geometry Defaults

```yaml
units: mm
width_mm: 5200
height_mm: 5100
lamella_count: 13
rows: 18
curve_samples: 9
attractor_x_mm: -900
attractor_z_mm: 2600
attractor_strength_mm: 520
lamella_depth_mm: 140
lamella_y_thickness_mm: 90
shingle_width_mm: 260
shingle_height_mm: 430
shingle_thickness_mm: 18
shingle_tilt_deg: 15
shingle_standoff_mm: 20
top_beam_depth_mm: 220
```

## Links

- `docs/errors/grasshopper-mcp-error-library.md`
- `docs/tools/grasshopper-workflow.md`
- `docs/tools/grasshopper-csharp-script-nodes.md`
- `scripts/grasshopper/examples/pavilion_80hz_lamella_attractor_csharp.cs`
