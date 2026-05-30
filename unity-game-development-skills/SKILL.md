---
name: unity-game-development
description: Comprehensive guidelines for building, modifying, and delivering Unity game projects with an AI agent. Use whenever the user asks to create, refactor, debug, or extend Unity (C#) game code, scenes, prefabs, ScriptableObjects, UI, gameplay systems, or platform builds (PC / Mobile / WebGL / 微信小游戏 / 抖音小游戏). English triggers — Unity, MonoBehaviour, prefab, scene, ScriptableObject, Addressables, Input System, URP, HDRP, "make a Unity game / Unity demo / Unity prototype". Chinese triggers — Unity / 做一个 Unity 小游戏 Unity 原型 / Unity 项目结构 / Unity 性能优化 / 微信小游戏 Unity / 抖音小游戏 Unity.
---

# Unity Game Development Skill

## Overview

This skill turns the agent into a disciplined Unity game developer. Its purpose is not to "produce code that compiles" but to deliver Unity projects that are **runnable, structured, maintainable, verifiable, and platform-aware**, evolving smoothly from a 30-minute demo to a production game.

The skill encodes:

1. A working philosophy (minimum playable loop first, then polish).
2. A canonical project layout and naming convention.
3. Concrete C# / MonoBehaviour / ScriptableObject patterns.
4. Performance and multi-platform constraints (Mobile / WebGL / 微信小游戏).
5. A delivery checklist and required reply format.

## When to Use

Activate this skill on ANY of the following signals:

- User mentions: Unity, Unity 6, MonoBehaviour, GameObject, Prefab, Scene, ScriptableObject, Addressables, Input System, URP, HDRP, Animator, Rigidbody.
- Request to write/modify a `.cs` file under `Assets/`.
- Request to "make a Unity demo / 原型 / 小游戏 / WebGL build / 微信小游戏 / 抖音小游戏".
- Request to design game systems (player controller, level system, UI manager, save system, object pool).
- Refactoring or reviewing an existing Unity project.

If the task is purely H5/JavaScript or non-Unity engine (Godot, Unreal, Cocos), do NOT use this skill.

## Core Principles (must follow, in order)

1. **Understand before modifying.** Inspect `Assets/`, `Packages/manifest.json`, `ProjectSettings/`, existing Scenes, Scripts, Prefabs, ScriptableObjects, and Addressables/Resources usage BEFORE creating files.
2. **Minimum playable loop first.** Deliver `Start → Input → Feedback → Win/Lose → Restart` before any polish, system, or content.
3. **Inspector-friendly always.** Expose tunables via `[SerializeField]`. Never hardcode magic numbers that a designer would want to tweak.
4. **Do not refactor user assets without permission.** No mass renames, moves, deletions, version upgrades, render-pipeline swaps, or `ProjectSettings` edits unless explicitly requested. State impact first.
5. **Every change must be verifiable.** State files changed, manual Inspector wiring required, and Play Mode validation steps.
6. **Code must compile.** No invented APIs, no missing `using`s, class name must match file name, no Editor APIs leaking into Runtime.

## Required Workflow

Follow this order on every Unity task:

### Step 1 — Discover

Read project state. **For the full discovery checklist (Unity version,
render pipeline, Active Input Handling, scripting backend, Domain Reload
state, project layout root) see `references/discovery-checklist.md`.**
At minimum:

- `Packages/manifest.json` + `ProjectSettings/ProjectVersion.txt` (Unity version, render pipeline, Input System, Addressables, DOTween, etc.)
- `ProjectSettings/GraphicsSettings.asset` (render pipeline) and
  `ProjectSettings/ProjectSettings.asset` (Active Input Handling, scripting backend, API level)
- `ProjectSettings/EditorSettings.asset` (Domain Reload — affects every static singleton / EventBus)
- `Assets/_Project/` or whatever root the user uses; existing `GameManager`, `UIManager`, scene composition
- Whether project uses **legacy `Input`** or **new `Input System`** — never mix
- Workspace-level context files: `GDD.md`, `游戏设计文档.md`, existing `H5-Demo/` or other prototype folders, `README.md`. If the user has a design doc or a JS/H5 prototype, read it before designing systems and reuse its data structures / level layouts / scoring rules.

If layout is missing, propose the canonical structure (see `references/project-structure.md`) but do not create empty folders unless the user agrees.

### Step 2 — Plan the minimal loop

Before writing code, in 1 short paragraph state:

- Game goal
- Player input
- Core objects
- State changes
- Win condition / Lose condition
- Restart flow

### Step 3 — Implement

Write code following the patterns in:

- `references/coding-standards.md` — naming, MonoBehaviour discipline, pure C# split
- `references/gameplay-patterns.md` — GameManager state machine, events, pooling
- `references/ui-input.md` — UI/Input separation
- `references/data-config.md` — ScriptableObject usage

When repeating common scaffolding (GameManager, EventBus, simple ObjectPool, Singleton MonoBehaviour, UI HUD, InputReader, IL2CPP `link.xml`), prefer adapting the templates in `assets/templates/` instead of rewriting from scratch. Read them with the `read_file` tool, then customize.

> **Template file extension convention.** Templates ship as `*.cs.txt`
> (and `*.xml.txt` for non-code) *only* so this skill repository itself
> is not compiled / consumed by Unity. When you drop a template into a
> Unity project you MUST:
>
> 1. Strip the trailing `.txt` (final filename: `MonoSingleton.cs`,
>    `EventBus.cs`, `InputReader.cs`, `link.xml`, ...).
> 2. Place it under the correct location:
>    - Runtime `.cs`: under `Assets/_Project/Code/Runtime/...`, never in
>      `Editor/`.
>    - `link.xml`: directly under `Assets/` (or any subfolder — Unity
>      picks up every `link.xml` in the project).
> 3. For `.cs`, adjust the namespace to match the project's existing
>    namespace (default is `Project.Core` / `Project.Systems` /
>    `Project.Input`). For `link.xml`, replace the placeholder
>    `Project.Runtime.*` with the project's actual assembly / namespace.
>
> Copying the file with `.txt` intact will leave Unity unaware of it —
> scripts won't compile, `link.xml` won't preserve types.

To bootstrap a new empty Unity project layout, run:

```
python3 scripts/init_unity_project_structure.py --path <Assets-folder-absolute-path>
```

This creates the `_Project/` skeleton (Art / Audio / Code / Configs / Prefabs / Scenes / Addressables / StreamingAssets) without touching existing files. Pass `--with-resources` only if the project intentionally uses a `Resources/` folder; the default omits it to discourage accidental abuse (Addressables is preferred).

### Step 4 — Verify

Before claiming completion, mentally walk through the **Delivery Checklist** in `references/delivery-checklist.md`. Do NOT claim "done" without it.

### Step 5 — Report

Reply to the user using the exact format defined in `references/delivery-checklist.md` (完成内容 / 文件变更 / Unity 中需要操作 / 验证方式 / 注意事项).

## Quick Reference (most violated rules — at-a-glance)

| ❌ Avoid | ✅ Do |
|---|---|
| `FindFirstObjectByType` / `GameObject.Find` in `Update` (and never `FindObjectOfType` — it is obsolete in Unity 6) | Cache references in `Awake`/`Start` |
| Logic inside UI `Button.onClick` | Forward to a system; UI only displays/forwards |
| Mutating ScriptableObject at runtime | SO = default config, separate runtime model |
| Hardcoded numbers | `[SerializeField] private float xxx;` |
| Mixing legacy `Input` with new Input System | Pick one and stick to it |
| Editor API in Runtime scripts | Move to `Assets/_Project/Code/Editor/` + `*.asmdef` |
| Mass `Instantiate`/`Destroy` of bullets/effects | Object pool |
| One mega-`GameManager` | Split into focused systems (`LevelManager`, `UIManager`, `AudioManager`, `InputReader`, `PoolManager`, ...) |
| Static singleton / `EventBus` without `[RuntimeInitializeOnLoadMethod]` reset | Reset statics on `SubsystemRegistration` (Domain Reload safety) |
| Claiming done without Play Mode validation | Provide explicit validation steps |

The full hard-ban list lives in `references/delivery-checklist.md` (`禁忌`
section). When in doubt, that file is authoritative — this table is just
the headline.

## Platform-Specific Constraints

When the target is Mobile, WebGL, 微信小游戏 or 抖音小游戏, additionally consult `references/performance-platform.md` BEFORE writing code. Key rules:

- Control draw calls, transparent overlap, texture size, audio compression.
- Avoid per-frame GC allocations (boxing, `string +`, LINQ in hot paths, `new` in `Update`).
- Use Addressables for big or remote assets; do not mix Addressables with `Resources/` chaotically.
- 微信/抖音小游戏: control 首包大小, use 分包, mind platform API differences, mind runtime memory peaks.

## What This Skill Will NOT Do

- Pick a render pipeline for the user without asking.
- Upgrade Unity or package versions unprompted.
- Delete or rename existing user files.
- Generate pseudo-code, fictitious Unity APIs, or scripts that won't compile.
- Skip the verification + reporting steps.

## Working with Unity MCP servers (when available)

Some environments connect a Unity Editor MCP server (e.g., `coplay-mcp`)
that exposes tools like `create_game_object`, `add_component`,
`set_transform`, `assign_material`, `save_scene`, `play_game`,
`get_unity_logs`. When such tools exist:

- **Prefer MCP for Editor-side state changes.** Creating GameObjects,
  wiring components, assigning materials, saving scenes — do them via the
  MCP tools instead of telling the user to drag things in the Inspector.
  This collapses the "Unity 中需要操作" step from a manual checklist into
  an executed action.
- **Still produce real `.cs` files.** Code goes through `write_to_file`
  to disk; MCP is for Editor manipulation, not source authoring.
- **Verify via MCP.** Use `get_unity_logs` / `check_compile_errors` /
  `play_game` to confirm the build is green before reporting "完成".

If no MCP server is present, fall back to the standard pattern: write
files, then enumerate the manual Inspector wiring in the report.

## Resources

- `references/discovery-checklist.md` — six-file pre-flight read for any new task
- `references/project-structure.md` — canonical Assets/_Project layout + naming rules
- `references/coding-standards.md` — C# style, MonoBehaviour vs pure C#, events, Domain Reload safety, debugging
- `references/gameplay-patterns.md` — GameManager state machine, event decoupling, scene/prefab discipline, animation (Awaitable / tween), physics
- `references/ui-input.md` — UI hierarchy, panel/HUD pattern, legacy Input vs Input System, uGUI vs UI Toolkit
- `references/data-config.md` — ScriptableObject configs, runtime model separation, Addressables handle anti-pattern
- `references/performance-platform.md` — Update hygiene, pooling, Mobile/WebGL/小游戏 constraints (incl. Task.Run / 反射 / 音频 / PlayerPrefs traps)
- `references/delivery-checklist.md` — verification checklist + required reply format + 禁忌 list
- `assets/templates/` — drop-in C# templates (GameManager, EventBus, ObjectPool, Singleton, HUDView, InputReader)
- `scripts/init_unity_project_structure.py` — generate the `_Project/` directory skeleton

When a task touches a specific area (e.g., UI work), load only the relevant reference file rather than all of them.
