# Source Card - 2DPlanTo3D

Repo: https://github.com/StepanKukharskiy/2DPlanTo3D

Status in our pipeline: useful reference for future plan/image intake.

## What It Gives Us

The useful part is the image-to-contour pattern:

```text
image
-> canvas / raster preprocessing
-> binary threshold
-> Moore contour tracing
-> RDP simplification
-> normalized profile polygons
```

For us, this is an intake tool, not a complete model builder.

## Useful Source Files In That Repo

```text
src/lib/contour-tracer.js
src/routes/+page.svelte
src/routes/images/+server.js
src/lib/components/Canvas3D.svelte
```

## How To Use In Our Scenarios

Scenario 1 - Reference to model:

- Extract footprint/profile candidates from plans, roof plans, silhouettes, or
  clean diagram images.
- Use extracted contours as proposals, then validate source authority.
- Convert to Rhino curves or build123d profiles only after scale and role are
  known.

Scenario 2 - Complex model cleanup:

- Usually not primary.
- May help create diagnostic section silhouettes from raster exports.

Scenario 3 - Massing and revisions:

- Can convert redline/plan sketches into footprint constraints.

## Critical Rule

Plan contour extraction is not source authority by itself.

Before using a contour as geometry, classify the drawing:

- exterior footprint;
- slab edge;
- balcony edge;
- load zone;
- core diagram;
- interior plan;
- annotation or scale marker.

Grove at Grand Bay lesson: a contour can represent the exterior slab/balcony
edge, while the glass line must be offset inward.

## Local Backlog

- Port the core idea to Python/OpenCV.
- Output `reports/contours.json`.
- Include scale, source type, confidence, and warnings.
- Preserve original image/underlay reference for review.
