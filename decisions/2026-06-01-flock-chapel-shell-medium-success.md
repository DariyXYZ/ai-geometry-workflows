# 2026-06-01 - Flock chapel shell medium success

## Context

The user provided a new Rhino/Aurox reference case with a scaled roof plan,
elevations, sections, and photos. The target is a low concrete wave/ribbon shell
building with glass walls and timber posts below the shell.

Source authority:

- scaled Rhino plan underlay: footprint size, roof length/depth, support/plinth
  positions;
- sections/elevations: crest height, valley height, top/bottom apex datums,
  ground/contact relationship;
- photos: visual confirmation of shell thickness, rim, concrete material, and
  wave rhythm.

## What worked

The first generated model was a medium success. It captured the broad family of
the object:

- a continuous concrete shell rather than a flat roof;
- alternating crests and valleys;
- recognizable wave/ribbon reading;
- visible rim/thickness cue.

The user confirmed it was "almost" and much closer than a generic surface.

## What failed

Three gates failed:

1. Secondary elements were premature and wrong. Glass, posts, mullions, and
   similar elements were created before the shell massing was accepted. They
   protruded below the shell and were misaligned.
2. The shell footprint was too long relative to the scaled plan. The user had
   to compress it manually. Because the plan was explicitly in scale, this is a
   source-authority failure.
3. The support logic was missing. The shell should sit on the concrete folded
   supports/plinths shown in the plan and sections. It must not read as
   floating above ground.

## Rule

For this family, do not detail under the shell until the shell and support logic
are proven.

Correct sequence:

```text
read scaled plan bbox / roof footprint
-> build shell only
-> check shell length/depth against plan underlay
-> add concrete folds / plinth supports at low contact lines
-> add thickness / rim
-> add glass, posts, mullions after acceptance
```

Secondary elements are not harmless context. If they are below the shell or
misaligned, they confuse review and should be omitted until the massing/support
gate passes.

## Next attempt

Start from the user-adjusted shell size if it remains in Rhino. Otherwise
rebuild a smaller shell directly against the plan underlay. Add only the
concrete folded support bases before any glass or timber elements.
