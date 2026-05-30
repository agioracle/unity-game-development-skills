# Unity Game Development Skills

English | [简体中文](README.zh-CN.md)

AI Agent Skill for building, refactoring, reviewing, and shipping Unity games.

This repository provides a Unity game development skill package for AI agents. It includes development workflows, project conventions, checklists, reusable templates, and helper scripts. It is not a Unity project that should be opened directly in Unity Editor. Instead, it is a guidance package for helping agents work more reliably inside real Unity projects.

## When to Use This Skill

Use this skill when a task involves:

- Creating, modifying, or debugging Unity game projects
- Writing `MonoBehaviour`, `ScriptableObject`, Prefab, Scene, UI, input, or gameplay systems
- Building a minimum playable loop, level flow, `GameManager`, object pool, event bus, or other gameplay foundations
- Working with Addressables, save data, localization, TextMeshPro, Input System, and other common Unity modules
- Preparing builds or optimizations for PC, mobile, WebGL, WeChat Mini Game, Douyin Mini Game, and similar platforms
- Reviewing Unity project structure, code quality, performance, or release readiness

## Skill Directory

The skill directory is:

```text
unity-game-development-skills
```

## Repository Layout

```text
.
├── README.md
├── README.zh-CN.md
├── LICENSE
└── unity-game-development-skills/
    ├── SKILL.md
    ├── references/
    ├── assets/
    │   └── templates/
    └── scripts/
```

| Path | Description |
| --- | --- |
| `unity-game-development-skills/SKILL.md` | Main skill entry point. Defines triggers, principles, workflow, and delivery format. |
| `unity-game-development-skills/references/` | Unity development conventions, platform constraints, checklists, and focused guides. |
| `unity-game-development-skills/assets/templates/` | C# / XML templates that can be copied into Unity projects. They use `.txt` to avoid accidental compilation. |
| `unity-game-development-skills/scripts/` | Helper scripts, currently including a Unity project structure initializer. |
| `LICENSE` | MIT License. |

## Installation

Copy the whole skill directory into your agent's skills directory:

```text
unity-game-development-skills/
```

The entry file is:

```text
unity-game-development-skills/SKILL.md
```

Different agents may use different skill installation locations. Follow the installation instructions for the agent tool you use.

## Recommended Workflow

`SKILL.md` defines the standard workflow for Unity tasks:

1. **Discover**: Inspect the project state first, including Unity version, packages, ProjectSettings, render pipeline, input system, and existing folder structure.
2. **Plan**: Define the minimum playable loop and the files to change before implementing. Avoid unnecessary large refactors.
3. **Implement**: Follow the coding, gameplay, UI/input, data/config, performance, and platform guidance.
4. **Verify**: Use the delivery checklist to confirm the work can compile, be verified, and be iterated on.
5. **Report**: Summarize completed work, changed files, Unity-side actions, verification steps, and important notes.

## Reference Documents

| Document | Content |
| --- | --- |
| `unity-game-development-skills/references/discovery-checklist.md` | Project discovery checklist before starting a Unity task. |
| `unity-game-development-skills/references/project-structure.md` | Recommended `Assets/_Project/` layout, naming rules, and asmdef placement. |
| `unity-game-development-skills/references/coding-standards.md` | C#, `MonoBehaviour`, lifecycle, event subscription, and Domain Reload conventions. |
| `unity-game-development-skills/references/gameplay-patterns.md` | Gameplay architecture patterns for `GameManager`, levels, object pools, Prefabs, and scene responsibilities. |
| `unity-game-development-skills/references/ui-input.md` | UI responsibilities, Canvas hierarchy, Safe Area handling, and legacy/new input system guidance. |
| `unity-game-development-skills/references/data-config.md` | `ScriptableObject` configs, runtime data, Addressables, save data, and localization guidance. |
| `unity-game-development-skills/references/performance-platform.md` | Update hot paths, GC, object pooling, mobile, WebGL, mini-game platforms, and IL2CPP stripping notes. |
| `unity-game-development-skills/references/delivery-checklist.md` | Pre-delivery checklist, response format, and hard rules for Unity tasks. |

## Templates

Templates are located in:

```text
unity-game-development-skills/assets/templates/
```

| Template | Suggested Unity project path | Purpose |
| --- | --- | --- |
| `EventBus.cs.txt` | `Assets/_Project/Code/Runtime/Core/EventBus.cs` | Type-safe event bus. |
| `GameManager.cs.txt` | `Assets/_Project/Code/Runtime/Core/GameManager.cs` | Basic game state machine. |
| `HUDView.cs.txt` | `Assets/_Project/Code/Runtime/UI/HUDView.cs` | HUD presentation-layer template. |
| `InputReader.cs.txt` | `Assets/_Project/Code/Runtime/Input/InputReader.cs` | Input reader template for the new Input System. |
| `MonoSingleton.cs.txt` | `Assets/_Project/Code/Runtime/Core/MonoSingleton.cs` | Generic `MonoBehaviour` singleton base class. |
| `SimpleObjectPool.cs.txt` | `Assets/_Project/Code/Runtime/Systems/SimpleObjectPool.cs` | Simple object pool implementation. |
| `link.xml.txt` | `Assets/link.xml` | IL2CPP / Managed Code Stripping preservation config template. |

When using templates:

- Remove the `.txt` suffix after copying a template into a Unity project.
- Adjust namespace, assembly references, and dependencies for the target project.
- Do not drag the whole skill repository into a Unity project as compilable code.
- `InputReader.cs.txt` depends on Unity's new Input System and assumes a generated `GameInput` C# class.
- `HUDView.cs.txt` uses TextMeshPro via the `TMPro` namespace.

## Initialize a Unity Project Structure

Use the helper script to create the recommended folder structure under a target Unity project's `Assets` directory:

```bash
python3 unity-game-development-skills/scripts/init_unity_project_structure.py --path /absolute/path/to/UnityProject/Assets
```

By default, the script creates an `_Project` folder tree and `.gitkeep` files under `Assets`. It does not create scripts, scenes, or Prefabs, and it does not modify `Packages`, `ProjectSettings`, or existing files.

Optional arguments:

```bash
# Set a custom project asset root name
python3 unity-game-development-skills/scripts/init_unity_project_structure.py --path /absolute/path/to/UnityProject/Assets --root MyProject

# Explicitly create a Resources directory
python3 unity-game-development-skills/scripts/init_unity_project_structure.py --path /absolute/path/to/UnityProject/Assets --with-resources

# Skip .gitkeep files
python3 unity-game-development-skills/scripts/init_unity_project_structure.py --path /absolute/path/to/UnityProject/Assets --no-gitkeep
```

Recommended layout example:

```text
Assets/_Project/
├── Art/
├── Audio/
├── Code/
│   ├── Runtime/
│   ├── Editor/
│   └── Tests/
├── Configs/
├── Prefabs/
├── Scenes/
├── Addressables/
└── StreamingAssets/
```

`Resources/` is not created by default. Use `--with-resources` only when it is explicitly needed.

## Unity Project Guidance

- Check Unity version, render pipeline, input system, scripting backend, and target platform before making changes.
- Build the minimum playable loop first, then expand presentation, levels, assets, and platform adaptation.
- Avoid frequent `FindObjectOfType`, `GetComponent`, LINQ, boxing, and temporary allocations in runtime hot paths.
- Keep `MonoBehaviour` classes as Unity glue where possible, and move core business logic into plain C# classes.
- Use `ScriptableObject` for static configuration; keep runtime state in separate runtime models.
- For IL2CPP, WebGL, or mini-game platforms, pay attention to stripping, file-system limitations, audio unlock behavior, memory peaks, and async loading constraints.

## License

This project is licensed under the [MIT License](LICENSE).
