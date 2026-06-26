# Grasshopper C# Performance

Status: active rules promoted from the local `grasshopper-script-nodes` skill
and project sessions.

Use this file when a Grasshopper C# Script node should have automatic inputs,
handle many items, run quickly, or avoid blocking Grasshopper.

## Goal

Write C# Script nodes that are:

- paste-ready in Rhino 8 Grasshopper;
- automatic in their visible IO when pasted into the script editor;
- idle-safe when inputs are disconnected;
- fast enough for interactive sliders;
- explicit about where parallel work is safe.

## Automatic IO Through Signature

The intended interface belongs in `RunScript(...)`:

```csharp
private void RunScript(
  List<Curve> Sections,
  int FloorCount,
  double FloorHeight,
  bool GenerateRails,
  ref object Floors,
  ref object Rails,
  ref object Info)
```

Rules:

- Use the signature to name inputs and outputs; do not rely on manual renaming
  instructions when the code can express the interface.
- Use typed inputs for the intended access shape:
  - `double`, `int`, `bool`, `Curve`, `Brep`, `Mesh` for item access;
  - `List<T>` for list access;
  - tree access only when branch paths are semantically meaningful.
- Avoid default `x/y/out/a` in production examples. Those names are acceptable
  only for smoke tests or when forced by a known automation limitation.
- Initialize outputs at the top of `RunScript` with empty lists, `null`, or a
  short status string.
- Keep missing optional inputs neutral; warn only when connected data is invalid.

## Item, List, And Tree Access

Choose access deliberately:

| Need | Prefer | Why |
| --- | --- | --- |
| One parameter controls the whole result | `double`, `int`, `bool` | Stable slider interaction |
| Repeated independent geometry | `List<T>` | One component solve, one output list |
| Parallel per-item work | `List<T>` plus indexed arrays | Safe deterministic order |
| Branch-preserving operations | tree input/output | Only when paths matter |
| Source curves grouped by floor/zone | tree or grouped output | Avoid lossy flattening |

Avoid accidental `Item` access for source geometry that should be processed as a
set. `Single Item` access can make Grasshopper run the script once per item,
which is slower and harder to validate.

## Parallel Computation

Use parallelism only for pure computation over independent items.

Safe candidates:

- numeric calculations;
- point/curve sampling when each item is independent;
- constructing independent `Point3d`, `Vector3d`, `Line`, `Polyline`,
  lightweight `Mesh` fragments;
- per-floor/per-panel metadata calculation.

Avoid parallel calls for:

- `RhinoDoc` reads or writes;
- baking objects;
- adding runtime messages;
- mutating shared `List<T>` instances;
- touching Grasshopper component state;
- operations whose RhinoCommon thread-safety is unknown.

Pattern:

```csharp
var results = new Brep[count];

System.Threading.Tasks.Parallel.For(0, count, i =>
{
  results[i] = BuildIndependentFloor(i);
});

Floors = results.Where(x => x != null).ToList();
```

Rules:

- Write into pre-sized arrays by index, not shared lists.
- Convert arrays to lists after the parallel block.
- Keep all `RhinoDoc` and Grasshopper side effects outside the parallel block.
- If an API is ambiguous or mutates shared geometry, run sequentially.
- For small counts, prefer sequential loops; parallel overhead can be slower.

## Caching

Cache only when recomputation is visibly expensive and inputs can be compared
cheaply.

Good cache keys:

- scalar parameters such as count, height, tolerance, mode;
- input object runtime serial numbers or stable ids when available;
- compact hashes of source point/curve counts.

Avoid caching:

- transient `RhinoDoc` object references;
- geometry that may be mutated downstream;
- results whose validity depends on hidden document state.

If caching inside a script node, keep it simple:

```csharp
private string _lastKey;
private List<Curve> _lastCurves;
```

Invalidate the cache whenever any meaningful input changes. Prefer correctness
over clever cache reuse.

## Geometry Performance Defaults

- Use `List<T>` with an expected capacity when building many outputs.
- Prefer arrays when output count is known.
- Avoid repeated expensive boolean operations inside slider loops.
- Generate massing/blockout first; add facade detail only after preview passes.
- Keep preview output counts controlled: hundreds are fine, tens of thousands
  need a density input or display mode switch.
- Expose counts and tolerances as inputs with practical defaults.
- Do not bake from a script node during ordinary preview solves.

## RhinoCommon Safety

Use the conservative geometry rules in:

```text
docs/tools/grasshopper/grasshopper-csharp-script-nodes.md
docs/errors/grasshopper/grasshopper-mcp-error-library.md
```

Known local rules:

- Include `using Rhino;` when using `RhinoDoc`.
- Use `Surface.CreateExtrusion(curve, vector).ToBrep()` and then
  `CapPlanarHoles(tolerance)` for closed section extrusions.
- Do not call `Brep.CreateFromExtrusion` without local verification.
- Treat `Curve.DivideByCount` as returning parameters; call `curve.PointAt(t)`.
- Do not reassign a `foreach` iteration variable.
- Verify ambiguous surface, trim, orientation, intersection, and projection APIs
  against local docs or the curated gotcha list before relying on them.

## Validation Gates

Before promoting a C# Script node:

```text
compile
-> check visible input/output names
-> solve with disconnected optional inputs
-> solve with default sliders
-> verify output counts and units
-> test a low/high slider range
-> record errors or reusable patterns in docs
```

For automated source assignment:

```text
SetSource
-> SetParametersFromScript
-> TryGetSource
-> inspect Params.Input / Params.Output
-> solve tiny script
-> only then use for production
```

If IO stays as `x/y/out/a`, stop using that route for automatic IO and switch
to manual paste-ready workflow.
