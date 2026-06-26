# Recent Rhino Case Lessons

Date: 2026-06-04

This file captures recent Rhino/RhinoMCP modeling results that should survive a
fresh chat. It is intentionally compact: it records source authority,
constructive grammar, what worked, what failed, and the reusable modeling rule.

## Infinity Tower / SOM

Status: partial success after correction.

Source authority:

- User-prepared Rhino curves override approximate parametric guesses.
- The exact floor contour, core circle, and height/twist axis are the primary
  sources for this case.

Main error:

- The first attempt replaced the actual section with a simplified square-like
  section even though the drawing and user curve showed a specific soft
  asymmetric contour.

Improved rule:

```text
visible user curves
-> classify floor contour / core / axis
-> verify units and height
-> transform exact contour copies through height
-> loft / floors / facade guides from those transformed copies
```

Do not treat "one section rotates with height" as permission to invent the
section.

## Shanghai Tower-Style Twisted Shaft

Status: improved, not fully accepted.

Source authority:

- Text gave 632 m height, 128 above-grade floors, and 180 degree total section
  rotation.
- Plan/reference images showed a soft triangular section with a corner bite.

What improved:

- The model moved from an organic blob to a soft triangular plan.
- Four main control sections were enough to validate the first loft.
- The corner cut became visible enough to create the intended spiral groove.

Main errors:

- Earlier versions read as rounded "dumpling" forms rather than triangular
  sections.
- Rotated square cutters were drawn next to the sections but did not actually
  drive the section cut.

Required grammar:

```text
soft triangle
minus rotated square/diamond cutter
-> cutter depth changes by height
-> 4 control sections
-> loft validation
-> Contour floors only after form acceptance
```

If a cutter is shown, the final curve must be derived from that cutter through
trim, boolean, split, or an explicit intersection algorithm.

## Flock Chapel Shell

Status: medium-success massing.

Source authority:

- Scaled plan underlay controls footprint, length/depth, and support/plinth
  locations.
- Sections control crest/valley heights and ground/contact logic.
- Photos control shell reading, material, rim thickness, and visual check.

What worked:

- The roof began to read as a wave/ribbon concrete shell.
- Alternating crests and valleys were recognizable.

Main errors:

- Glass, posts, and mullions were added before the shell was accepted and
  protruded below it.
- The shell was too long relative to the scaled plan.
- The shell floated instead of bearing on the concrete folded/plinth supports.

Required order:

```text
scaled plan footprint
-> section-derived crest/valley heights
-> shell surface only
-> fit check against plan
-> concrete folded supports/plinth at contact lines
-> thickness/rim
-> glass/posts only after shell/support acceptance
```

## Symmetric Stepped Residential Tower

Status: useful failure/correction case for simple massing grammar.

Source authority:

- Plans define three footprint types: cross, half-cross, rectangle.
- Elevation/text define 59 m height and fixed 27 m x 38.9 m envelope.
- User clarified vertical symmetry: cross, half-cross, rectangle, half-cross,
  cross.

Main errors:

- Some attempts changed the overall footprint size per band, creating an
  unintended taper.
- One run stacked all floors at the same Z level.
- Context brick building proportions were too narrow and not close enough to
  the plan.

Required grammar:

```text
same 27 m x 38.9 m bbox for all plan types
-> draw cross / half-cross / rectangle footprints
-> extrude each 3-floor band at the correct Z
-> preserve vertical symmetry
-> context massing follows site-plan proportion
```

For stacked massing, Z placement is part of the geometry grammar, not an
afterthought.

## Aqua Tower / Studio Gang

Status: successful video demonstrator.

What worked:

- Rectangular tower core plus floor-by-floor wavy balcony slabs produced a
  recognizable Aqua Tower reading.
- Thin base/podium worked better than the first oversized plinth.
- Slowed construction made the modeling process legible for video.
- Obsolete red height/construction lines were removed for clean capture.

Video/replay rules:

- Do not leave the tower floating above the base.
- Keep the base thin unless the reference calls for a large podium.
- Preserve the current Rhino camera when the user has already set the shot.
- Hide or delete helper lines that no longer explain an active operation.

Useful local script:

```text
.tmp_cases/20260529_172421_aqua-tower-wavy-balconies/scripts/build_aqua_wavy_tower_video_slow.py
```

## Absolute World Towers

Status: successful video demonstrator.

What worked:

- Two elliptical tower cores with gradual floor rotation read correctly for the
  case.
- Repeated floor rings plus twisted vertical guide lines communicated the
  building logic well enough for video.
- The construction could be rerun while preserving the user-set camera.

Useful local script:

```text
.tmp_cases/20260529_174623_absolute-world-towers-rotating-ellipses/scripts/build_absolute_world_towers_video_slow.py
```

## Cross-Case Rules

- First classify source authority: what is proven by text, plan, elevation,
  section, photo, and user-prepared Rhino curves.
- State constructive grammar before modeling.
- Prefer primitives and real modeling operations over blind point clouds.
- If the grammar includes a cutter, the cutter must produce the final cut.
- Build massing/proportion/support first; add secondary elements only after
  acceptance.
- Validate units, height, footprint, support/contact, and non-floating geometry.
- Preserve user-created source geometry and the user-selected camera.
- For video scripts, slow down visible construction and remove stale helper
  geometry before the final pass.
