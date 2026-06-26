# Rhino MCP Backend Policy

Status: active policy.

## Default

Use the official McNeel RhinoMCP server as the default Rhino transport:

```text
mcneel/RhinoMCP
https://github.com/mcneel/RhinoMCP
```

For Codex, the expected MCP config shape is:

```toml
[mcp_servers.rhino]
command = "rhino-mcp-router"
args = ["--default-version", "8"]
```

If no slot is visible, ask the user to run `MCPStart` in Rhino. Use the full
router executable path from the local `.mcp.json` or Rhino MCP package install
when configuring Codex; do not invent a path.

## Operating Rule

Do not hard-code Aurox as the default Rhino route in new docs, workflows, case
templates, or scripts.

Use Aurox, a custom Rhino bridge, or another plugin only when:

- the user explicitly asks for that backend;
- a legacy case already depends on that backend and the task is to replay it;
- the standard RhinoMCP tool surface lacks a required operation and the backend
  is chosen deliberately as a workaround.

When switching away from standard RhinoMCP, say which capability required the
switch and keep the workflow portable where possible.

## Third-Party MCP Rule

When the user asks for a third-party Rhino MCP/plugin backend, explicitly use a
RhinoCommon execution route for non-trivial geometry:

```text
third-party MCP/plugin
-> capability scan
-> RhinoCommon through run_python, run_csharp, execute_csharp, or equivalent
-> validate in the active Rhino document
```

Do not assume a third-party MCP's simplified geometry helpers cover the full
Rhino modeling surface. Use those helpers only after checking their schemas and
running a smoke test. For precise modeling, booleans, contours, trims, lofts,
sections, and object/layer audits, prefer RhinoCommon-backed execution.

## Working Order

```text
capability scan
-> standard RhinoMCP tools
-> Rhino command / Grasshopper operations exposed by RhinoMCP
-> RhinoCommon via run_python/run_csharp for complex geometry
-> third-party backend only when requested or required
-> record the backend-specific dependency in the case note
```

## Required Capability Scan

Before any Rhino geometry build or model review, inspect the active RhinoMCP
surface instead of assuming a fixed plugin/tool set:

1. `mcp__rhino.list_slots` - find the active slot or confirm auto-spawn.
2. `mcp__rhino.run_python` - print Rhino version, document name, object count,
   and current unit system from `__rhino_doc__`.
3. Set model units explicitly when the task declares a scale, for example
   meters for 1:1 architectural massing.
4. `mcp__rhino.get_commands` - sample required command families before using
   them, for example `Box`, `Layer`, `Boolean`, `Loft`, `Extrude`, `View`,
   `Grasshopper`, and `Python`.
5. Run a tiny smoke script with `__rhino_doc__` before a large build when using
   RhinoCommon through `run_python` or `run_csharp`.

Record the observed Rhino version and the relevant available command families
in the case note or final handoff.

## Legacy Aurox Notes

Older project memory, archives, and helper scripts may mention Aurox because
that was the previous bridge. Treat those as historical or optional-backend
instructions, not as default policy.
