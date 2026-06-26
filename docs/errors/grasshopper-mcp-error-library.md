# Grasshopper MCP Error Library

Status: active.

This file records failure modes observed or expected when automating
Grasshopper through RhinoMCP.

## GH-001 - `g1_start` Timeout Does Not Prove Failure

Symptom:

`g1_start` times out after a long wait.

Cause:

Grasshopper may still be loading, or Rhino may have a command queue state that
does not return cleanly to MCP.

Detection:

Run `g1_search_components` after the timeout. If component search works,
Grasshopper may be loaded even though `g1_start` timed out.

Correction:

For production work, avoid closing or spawning slots unless the user explicitly
asks for it. Ask the user to open Grasshopper manually and run `MCPStart` if no
RhinoMCP slot is visible.

Required gate:

Never proceed from `g1_start` timeout directly to a large graph. Run component
search and a tiny smoke placement first.

## GH-002 - Component Search Can Work Without An Active GH Document

Symptom:

`g1_search_components` returns components, but `g1_place_component` returns:

```text
Could not get or create GH document
```

Cause:

The Grasshopper component library is available, but no active canvas/document
exists.

Correction:

Ask the user to open Grasshopper manually in the connected Rhino slot, then
place a tiny graph.

Required gate:

Do not treat component search as proof that a canvas exists.

## GH-003 - `g1_apply_graph` Generic Failure

Symptom:

`g1_apply_graph` returns only:

```text
An error occurred invoking 'g1_apply_graph'.
```

Cause:

The batch call hides which step failed.

Correction:

Place sliders and components one by one, then wire one connection at a time.

Required gate:

Use `g1_apply_graph` only after the same graph has been proven manually, or for
simple repeatable graphs with known selectors.

## GH-004 - `Panel` Can Behave As A Value Source

Symptom:

Wiring to `Panel` fails with:

```text
destination '' is a value source, not an input
```

Cause:

The MCP selector semantics can treat Panel as a parameter/value source rather
than a standard component input.

Correction:

For first smoke tests, avoid Panel. Use visible preview geometry such as
`Construct Point`.

Required gate:

Do not use Panel as the only proof that solve worked.

## GH-005 - GH Preview Is Not A Rhino Document Object

Symptom:

`g1_solve_graph` succeeds, but Rhino viewport capture reports an empty document.

Cause:

Grasshopper preview geometry is not baked into the Rhino document.

Correction:

Validate solve success through `g1_solve_graph`, component outputs where
available, or bake/reference workflow when document geometry is required.

Required gate:

Do not mistake empty Rhino document object count for failed GH preview.

## GH-006 - Direct `g1_*` Script Source Setter Missing

Symptom:

`C# Script` or `Python 3 Script` can be placed and wired, but no exposed MCP
`g1_*` tool can set the component's code body.

Cause:

Current g1 tool surface exposes placement/wiring/solve but not script-source
editing. Source editing may still be available indirectly through the
Grasshopper .NET API.

Correction:

Store paste-ready script bodies in `scripts/grasshopper/` and use them manually
or through a proven source-setting bridge.

Required gate:

When a script component matters, commit its script body to the repo.

## GH-007 - Programmatic `SetSource` Can Keep Wrong IO

Symptom:

The Rhino 8 C# Script component accepts source through `SetSource(string)`, but
the component still shows default inputs/outputs such as:

```text
x
y
out
a
```

and `TryGetSource` shows that `RunScript(...)` has been rewritten to the
default signature.

Cause:

Programmatic source assignment into
`RhinoCodePluginGH.Components.CSharpComponent` is not equivalent to manually
pasting a classic `GH_ScriptInstance` script into the component editor. The
component may preserve the existing IO contract unless its expected source
format and parameter update path are proven.

Detection:

After `SetSource(...)`, inspect:

```text
TryGetSource
Params.Input
Params.Output
```

Do not rely on `SetSource` returning without error.

Correction:

Use `docs/tools/grasshopper-csharp-script-nodes.md`. Keep the code as a
paste-ready script in `scripts/grasshopper/examples/`, or use a legacy/dedicated
component route only after a tiny source-and-IO smoke test succeeds.

Required gate:

For any automated source injection, prove this sequence first:

```text
SetSource
-> SetParametersFromScript
-> inspect IO names
-> solve tiny script
```

If the IO names are wrong, stop before building the production graph.

## GH-008 - Ambiguous Duplicate Components

Symptom:

A search returns multiple components with the same display name, for example
`Addition`.

Cause:

Grasshopper has category-specific components with identical names.

Correction:

Use GUID selectors from `g1_search_components`, not names, once the exact
component has been identified.

Required gate:

For reusable graph builders, store GUIDs and the component category/subcategory
in comments or config.

## GH-009 - `g1_*` Calls Crash A User-Started (Adopted) Slot

Symptom:

On a Rhino slot started manually by the user (`MCPStart`, adopted into the
router), the first `g1_*` call crashes the entire Rhino process.

Observed 2026-06-22:

```yaml
rhino_version: 8.30.26103.11001
slot: aardvark
port: 10500
pid: 39872
adopted: true
call: g1_search_components(query="loft")
result: rhino_crashed, slot pruned, list_slots -> []
```

The Python/C# layer (`run_python`, `run_csharp`) on the same slot was stable and
returned a clean capability scan immediately before the crash.

Cause:

The g1 Grasshopper layer initialization (triggered lazily by the first `g1_*`
call) is unstable on an adopted slot. This matches the user-reported behavior
that auto-start of the GH layer hangs or crashes Rhino.

Detection:

`list_slots` returns `[]` right after a `g1_*` call returns `rhino_crashed`.

Correction:

Do NOT use any `g1_*` tool against a slot the user opened manually
(`g1_search_components`, `g1_start`, `g1_place_*`, `g1_apply_graph`,
`g1_solve_graph`, `spawn_slot`). Use the stable `run_python` layer for:

- capability scan (version, units, object count);
- Grasshopper component lookup (query the GH component server from Python, or
  rely on documented GUIDs);
- geometry validation of C# Script node logic (port the RhinoCommon body to
  `run_python`, bake and inspect) before any manual GH paste.

Prefer `run_python` over `run_csharp` for validation — `run_csharp` routes
through the RhinoCode C# engine and can wedge the plugin handler (see GH-012).

For C# Script node cases (e.g. the spiral skyscraper), the proven path is:
validate the RhinoCommon logic via `run_python`, then manually paste the script
body into a Rhino 8 `C# Script` component. No `g1_*` canvas automation is
required.

Required gate:

Never call a `g1_*` tool on an adopted/user-started slot. If a Grasshopper
canvas operation is genuinely required, ask the user before any
`g1_start` / `spawn_slot` and expect a possible crash.

Note:

This supersedes the detection steps in GH-001 and GH-002 that suggested running
`g1_search_components` as a probe. On an adopted slot that probe is the crash.

## GH-010 - Rhino Connect Command Is `MCPStart`, Not `MCPConnect`

Symptom:

Earlier workflow notes told the user to run `MCPConnect` in Rhino. There is no
such command in the standard McNeel `Rhino-MCP-Platform` plugin.

Cause:

Naming drift. The official McNeel RhinoMCP connector docs use `MCPStart` to load
and start the in-Rhino plugin. Confirmed 2026-06-22: after the user ran
`MCPStart`, the router advertised slot `aardvark` on `http://localhost:10500`.

Correction:

Ask the user to run `MCPStart` in Rhino (Yak package `Rhino-MCP-Platform`:
`yak install Rhino-MCP-Platform`). The Claude Desktop side uses the
`connector.mcpb` extension from GitHub releases.

Required gate:

Use `MCPStart` in all workflow/pattern docs and prompts. Do not instruct
`MCPConnect`.

## GH-011 - Competing `rhino-mcp-router` Instances Break Forwarded Calls

Symptom:

`list_slots` works and shows the slot as alive/adopted, but every forwarded
call (`run_python`, `run_csharp`, `g1_*`) returns:

```text
existing_rhino_unreachable -- The Rhino likely crashed. Stale slot pruned -- retry the call.
```

The slot immediately reappears in `list_slots` (the slot advertiser keeps
broadcasting), so it looks alive while no real call ever completes.

Observed 2026-06-22:

Two `rhino-mcp-router.exe` processes were running at once, each from a different
host application, both adopting the same Rhino slot:

```yaml
router_A: pid 26908, parent claude.exe   # this Claude Code session
router_B: pid 41308, parent codex.exe    # a separate Codex session
plus:      two stale rhinomcp.exe (parent uv.exe) -- a different community MCP server
slot:      aardvark, Rhino pid 29716, ports 10500 (dead) / 10501 (listening)
```

`list_slots` is a router-local registry read, so it answers fine. But two
routers contend for the single Rhino plugin HTTP endpoint, and forwarded calls
to the plugin time out.

Plugin-side signature (in the Rhino command-line / MCP log):

```text
[Rhino MCP] InvalidOperationException: Headers are read-only, response has already started.
  at ...HttpResponseHeaders...set_ContentType(StringValues value)
  at RhMcp.Server.McpDispatcher.WriteResponseAsync(HttpContext ctx, JsonRpcResponse response) McpEndpoint.cs:line 301
  at RhMcp.Server.McpDispatcher.HandleAsync(HttpContext ctx) McpEndpoint.cs:line 109
```

`Headers are read-only, response has already started` means the plugin tried to
write a response twice on the same `HttpContext` -- the fingerprint of two
routers racing concurrent forwards onto one request. This is an upstream McNeel
plugin bug (it sets `ContentType` after the response body has begun), but the
trigger here is the duplicate router. Once it throws, the dispatcher is wedged
and every later call times out (this is the plugin-side cause behind GH-012's
symptom).

Cause:

The McNeel router is launched per host application (each MCP client spawns its
own `rhino-mcp-router.exe`). When two AI clients (e.g. Claude Code and Codex)
are open against the same Rhino, both routers adopt the same advertised slot and
fight over forwarding. Concurrent forwards race in `McpDispatcher` and corrupt
the response, wedging the handler.

Detection:

```powershell
Get-Process rhino-mcp-router,rhinomcp |
  Select-Object Id, ProcessName,
    @{n='Parent';e={(Get-CimInstance Win32_Process -Filter ("ProcessId="+$_.Id)).ParentProcessId}}
# then map ParentProcessId -> claude.exe / codex.exe / uv.exe
Get-NetTCPConnection -State Listen | Where-Object LocalPort -ge 10500   # which port the plugin actually listens on
```

If more than one `rhino-mcp-router.exe` exists, identify each by parent process.

Correction:

Keep exactly one router for the active session. Kill the competing router(s) and
any unrelated `rhinomcp.exe` (the community server) by PID — never kill the
router whose parent is your own host process:

```powershell
Stop-Process -Id <competing_router_pid>,<stale_rhinomcp_pids> -Force
```

Killing a competing router belongs to another running AI session; confirm with
the user before stopping it.

Required gate:

Before deep RhinoMCP debugging, enumerate `rhino-mcp-router.exe` and map each to
its parent host. A single contended slot with multiple routers looks identical
to a crash. Note: removing the duplicate router does not by itself unwedge a
plugin handler already blocked by GH-012 -- a full Rhino restart may still be
needed.

## GH-012 - `run_csharp` (RhinoCode) Can Wedge The Plugin Handler

Symptom:

After a `run_csharp` call times out, the slot's port stays open and TCP connects
(`Test-NetConnection` succeeds), Windows reports the Rhino process as
`Responding: True`, yet every subsequent forwarded call -- including
`run_python` -- times out with `existing_rhino_unreachable`.

Observed 2026-06-22:

```yaml
rhino_pid: 29716
listening_port: 10501   # TCP connect succeeds
windows_responding: true
first_call_on_slot: run_csharp (full spiral-tower validation)
result: timeout, then every run_python/run_csharp also times out
```

On an earlier slot where `run_python` ran first (before any `run_csharp`), the
Python layer worked. The wedge appeared only after `run_csharp`.

Cause (suspected):

`run_csharp` routes through the RhinoCode C# engine. Its first use can pop a
modal/consent or compile step that does not register as a non-responding main
window, but blocks the plugin's single script-execution queue. Once blocked, the
queue never drains, so `run_python` (same queue) also hangs.

Detection:

```powershell
Test-NetConnection 127.0.0.1 -Port <slot_port>   # TcpTestSucceeded = True
Get-Process Rhino | Select-Object Id, Responding  # Responding = True
```

Port open + process responding + every forwarded call timing out = a wedged
plugin handler, not a crash (contrast GH-009, where the process dies and
`list_slots` empties).

Correction:

Prefer `run_python` for all validation and capability work. Reserve `run_csharp`
for cases where C# is strictly required, and accept the first call may need a
manual RhinoCode dialog dismissal in the Rhino UI. To recover a wedged slot:

1. Check the Rhino window for a hidden/behind RhinoCode or script dialog; close
   it.
2. If none, fully restart the Rhino process (kill the PID, relaunch, `MCPStart`).
3. On the fresh slot, smoke-test with `run_python` first; do not lead with
   `run_csharp`.

Required gate:

Lead every fresh slot with a `run_python` smoke, never `run_csharp`. For C#
Script node cases, validate the geometry logic in `run_python` and paste the C#
body manually into the Grasshopper component.

## GH-013 - Programmatic `SetSource` via Reflection Makes Component Non-Editable

Symptom:

After calling `SetSource(string)` on
`RhinoCodePluginGH.Components.CSharpComponent` via .NET reflection, the
component shows compile errors in the canvas and the Script Editor opens in a
read-only or non-interactive state — the user cannot paste or edit code inside
it.

Observed 2026-06-22:

```yaml
method: SetSource invoked via System.Reflection on CSharpComponent
result_in_canvas: compile errors "The name 'Floors' does not exist [27:30]"
result_in_editor: component non-editable, paste has no effect
recovery: user created a fresh C# Script from the toolbar, pasted code manually
```

Cause:

`SetSource` bypasses the Script Editor's compilation pipeline. The code is
stored internally but the component remains in an inconsistent state: it
compiles the source in a context that does not inject GH input parameters as
RunScript variables. The Script Editor then treats the component as already
compiled and does not offer the normal edit flow.

Distinction from GH-007:

GH-007 covers `SetSource` keeping wrong IO (x/y/out/a). GH-013 is the
downstream effect: after any reflection-based source manipulation, the
component can become fully non-editable through the UI.

Correction:

Do not call `SetSource` (or any `RhinoCodePluginGH` internal method) via
reflection to set GH1-style `GH_ScriptInstance` code. The only reliable path:

1. Place the component fresh from the GH toolbar (or via a proven g1 route on
   a non-adopted slot).
2. Double-click to open the Script Editor.
3. Ctrl+A → Ctrl+V to paste the paste-ready script body.
4. Close the Script Editor — the component compiles and IO is set from the
   RunScript signature automatically.

Sliders and wires can still be placed/connected programmatically via
`run_python` (see the spiral skyscraper case). Only the source paste requires
manual UI action.

Required gate:

Never use reflection-based `SetSource` on `RhinoCodePluginGH.Components.*` for
production graphs. Treat manual paste as the only proven source-injection path
for the modern Rhino 8 C# Script component.

## GH-014 - Modern C# Script Reserves First Output As `out`

Symptom:

After programmatically adding named outputs to
`RhinoCodePluginGH.Components.CSharpComponent`, the first visible output remains
the script console output `out`. A source body whose `RunScript` signature starts
with a production output such as `ref object VoxelBoxes` compiles with:

```text
The name 'VoxelBoxes' does not exist in the current context
```

Observed 2026-06-22:

```yaml
component: Rhino 8 C# Script
manual_params: out, VoxelBoxes, EnvelopeMesh, FloorOutlines, FacadeLines
actual_RunScript_after_SetSource: ref object EnvelopeMesh, ...
result: first production output dropped from signature
```

Cause:

The modern Rhino 8 C# Script component treats the first output slot as the
script console output `out`. It is visible in `Params.Output`, but it is not a
normal `ref object` output in the generated `RunScript` signature.

Correction:

Keep the first output named `out` and put production outputs after it:

```text
out
VoxelPoints
EnvelopeMesh
FloorOutlines
FacadeLines
PluginGuides
Metrics
Info
```

Write script bodies so the first `ref object` output in `RunScript` corresponds
to the second visible output after `out`.

Required gate:

After creating or editing a C# Script component programmatically, call
`TryGetSource` and inspect the actual `RunScript` signature, not only
`Params.Output`.

## GH-015 - Legacy C# `SourceCodeChanged(None)` Crashes Rhino

Symptom:

Programmatically editing the legacy `C# Script` component
(`ScriptComponents.Component_CSNET_Script`) and then calling:

```python
component.SourceCodeChanged(None)
```

crashes Rhino 8.30. The router prunes the slot as `rhino_crashed`.

Observed 2026-06-26:

```yaml
rhino_version: 8.30.26103.11001
grasshopper_version: 8.30.26103.11001
component: ScriptComponents.Component_CSNET_Script
operation: set ScriptSource.UsingCode / ScriptCode / AdditionalCode, then SourceCodeChanged(None)
result: Rhino crash before .gh save
crash: System.NullReferenceException at Component_AbstractScript_Roslyn.SourceCodeChanged(GH_ScriptEditor sender)
case: Pavilion 80hz lamella attractor
```

Cause:

`SourceCodeChanged` expects a real `GH_ScriptEditor` sender. Passing `None`
creates an asynchronous UI-thread `NullReferenceException`. The error is thrown
later through the dispatcher, so a local `try/catch` around the call does not
protect Rhino.

Correction:

Do not call `SourceCodeChanged(None)`. Do not trust legacy C# script-source
automation until a tiny disposable smoke test proves source refresh, IO, solve,
and save in the same Rhino/Grasshopper version.

Stable path:

```text
store paste-ready C# body in scripts/grasshopper/examples/
-> user creates fresh C# Script component
-> manual paste through Script Editor
-> Codex may automate surrounding sliders/groups only through proven run_python routes
```

Required gate:

If a task needs a C# Script node, the script body must exist in the repo before
any risky Grasshopper source-injection attempt. For Pavilion 80hz, use:

```text
scripts/grasshopper/examples/pavilion_80hz_lamella_attractor_csharp.cs
```
