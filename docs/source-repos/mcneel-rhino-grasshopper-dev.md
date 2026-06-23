# Source Card - McNeel Rhino And Grasshopper Developer Stack

Status: active official-source card.

Use this before searching random tutorials for RhinoCommon, Grasshopper C#,
plugin packaging, or official sample code.

## Sources

| Source | Link | Use |
| --- | --- | --- |
| McNeel Developer Docs | https://developer.rhino3d.com/ | First stop for official Rhino/GH development. |
| API References | https://developer.rhino3d.com/api | RhinoCommon and Grasshopper API lookup. |
| Grasshopper Guides | https://developer.rhino3d.com/guides/grasshopper | Custom GH components, scripting, algorithms. |
| Essential C# Scripting | https://developer.rhino3d.com/guides/grasshopper/csharp-essentials/ | C# Script component learning path. |
| RhinoCommon Geometry in GH C# | https://developer.rhino3d.com/guides/grasshopper/csharp-essentials/3-rhinocommon-geometry/ | Geometry classes/functions inside C# Script. |
| Rhino Developer Samples | https://github.com/mcneel/rhino-developer-samples | Official sample code for Rhino and GH ecosystem. |
| Rhino Package Manager | https://www.rhino3d.com/features/package-manager/ | Discover/install/manage plugins and GH components. |
| Yak Guides | https://developer.rhino3d.com/guides/yak/ | Package structure, publication, custom package sources. |
| Rhino.Inside.Revit | https://github.com/mcneel/rhino.inside-revit | Official Revit embedding and GH/Revit bridge. |
| RhinoMCP | https://github.com/mcneel/RhinoMCP | Default MCP transport for this repo. |

## What This Gives Us

- Official API semantics before guessing RhinoCommon return types.
- Sample code that can be translated into C# Script nodes or compiled plugins.
- Package Manager / Yak as the preferred plugin installation/distribution path.
- Rhino.Inside.Revit as the official BIM/Revit bridge for architecture tasks.
- RhinoMCP as the standard AI-agent transport.

## Workflow Rule

```text
AI request
-> repo workflow docs
-> official McNeel docs/API/samples
-> Food4Rhino plugin pages
-> community tutorials only for usage patterns
```

Do not base geometry logic on memory when RhinoCommon or Grasshopper API
semantics matter. Check official API/docs first, then encode any durable gotcha
in `docs/errors/` or `docs/tools/`.

## Package Manager Notes

Use Rhino Package Manager for plugin discovery and install when possible.
McNeel also calls the package tooling Yak.

Important implications:

- Prefer packaged plugins over loose `.gha` copies when available.
- Record plugin names exactly as they appear in Package Manager/Food4Rhino.
- For office/shared setups, Yak custom package sources can become a managed
  internal plugin distribution path.
- For our own future compiled GH plugin, follow Yak package structure:

```text
manifest.yml
*.rhp
*.gha
dependencies / misc files
```

## How To Use In This Repo

- For C# Script nodes: read `docs/tools/grasshopper-csharp-script-nodes.md`.
- For compiled plugins: use the local `grasshopper-plugin-development` skill.
- For architecture plugin routing: read
  `docs/libraries/grasshopper-architecture-plugin-stack.md`.
- For RhinoMCP transport policy: read `docs/source-repos/rhinomcp.md`.
