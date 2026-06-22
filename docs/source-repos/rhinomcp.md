# Source Card - McNeel RhinoMCP

Repo: https://github.com/mcneel/RhinoMCP

Docs: https://mcneel.github.io/RhinoMCP/

Status in our pipeline: default Rhino MCP backend.

## What It Gives Us

RhinoMCP is the official McNeel MCP server for AI agents to create and edit
geometry in Rhino and Grasshopper.

It is the default transport for Codex-driven Rhino work in this repository.

## Codex Setup Contract

Use Rhino `MCPConnect` to copy the router command when available. The documented
Codex config shape is:

```toml
[mcp_servers.rhino]
command = "rhino-mcp-router"
args = ["--default-version", "8"]
```

Use the full router executable path if Rhino prints one through `MCPConnect`.

## Backend Boundary

Default:

```text
Codex
-> mcp__rhino tools / RhinoMCP router
-> Rhino / Grasshopper scene operations
```

Optional:

```text
Codex
-> Aurox or another Rhino plugin
-> only by explicit user request or backend-specific need
```

Do not make Aurox a hidden dependency for new cases, docs, or scripts.

If a user explicitly selects a third-party Rhino MCP/plugin backend, require a
RhinoCommon execution route for non-trivial geometry and document the reason for
leaving standard RhinoMCP.

## Capability Scan Pattern

Use this before building geometry:

```text
list_slots
-> run_python version/units/object_count through __rhino_doc__
-> get_commands for the command families needed by the task
-> tiny run_python or run_csharp smoke-run
-> build
```

Observed test setup on 2026-06-22:

```yaml
server: Rhino-MCP-Platform 0.1.5 router
rhino_version: 8.30.26103.11001
available_tool_examples:
  - run_command
  - run_python
  - run_csharp
  - list_objects
  - set_selection
  - get_commands
  - Grasshopper graph operations
command_families_seen:
  Box: [Box, BoundingBox, SubDBox]
  Layer: [Layer, ChangeLayer, CopyToLayer]
  Boolean: [BooleanUnion, BooleanDifference, BooleanIntersection]
  Loft: [Loft, DevLoft, SubDLoft]
  Extrude: [ExtrudeCrv, ExtrudeSrf, ExtrudeMesh]
  View: [SetView, ViewCaptureToFile, NamedView]
  Python: [RunPythonScript, EditPythonScript]
```
