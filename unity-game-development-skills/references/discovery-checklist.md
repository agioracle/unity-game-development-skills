# Discovery Checklist (read BEFORE writing any code)

Unity projects diverge wildly in their basic settings, and the wrong
assumption (legacy Input vs new Input System, Built-in vs URP, Mono vs
IL2CPP, .NET Standard 2.1 vs .NET Framework, Domain Reload on/off) will
silently break otherwise correct code. Always inspect the following
**six** files / settings during Step 1 — Discover.

> Tip: most of these are plain YAML and can be read with `read_file`. None
> of them should be modified without explicit user permission.

## 1. `Packages/manifest.json` — Unity & package versions

Locate at minimum:

- Unity version (look at `ProjectSettings/ProjectVersion.txt` for the
  authoritative value — `manifest.json` only lists package versions).
- `com.unity.inputsystem` → if present, use the new Input System.
  If absent, use legacy `Input` or ask the user before adding the package
  (adding it requires changing `Active Input Handling`, which restarts the
  editor).
- `com.unity.addressables` → if present, prefer Addressables over
  `Resources/`.
- `com.unity.render-pipelines.universal` / `.high-definition` → tells you
  the active render pipeline family. Cross-check with item 3 below.
- `com.unity.localization`, `com.unity.cinemachine`, `com.unity.timeline`,
  DOTween — note their presence so you can use them instead of rolling
  your own.

## 2. `ProjectSettings/ProjectVersion.txt` — exact Unity version

```
m_EditorVersion: 6000.0.x
```

- `6000.x` = Unity 6 LTS. `Awaitable`, `FindFirstObjectByType` available.
- `2022.3.x` = Unity 2022 LTS. Most modern APIs available, but no
  `Awaitable`.
- Older → ask before assuming Unity 6 APIs.

## 3. `ProjectSettings/GraphicsSettings.asset` — Render Pipeline

Look for `m_CustomRenderPipeline` reference:

- Empty / `{fileID: 0}` → **Built-in Render Pipeline**. Standard shader,
  Camera + Light just work. URP-only Shader Graph nodes won't compile.
- Set to a `UniversalRenderPipelineAsset` → URP. Use URP-compatible
  shaders only (`Universal Render Pipeline/Lit`, etc.).
- Set to an `HDRenderPipelineAsset` → HDRP. Heavy on PC; almost never used
  for casual / mini-game targets.

**Never silently switch render pipeline.** It breaks every existing
material and post-process volume.

## 4. `ProjectSettings/ProjectSettings.asset` — Input / Backend / API Level

Search the YAML for:

- `activeInputHandler:`
  - `0` → legacy Input only
  - `1` → new Input System only
  - `2` → both (allowed but discouraged)
- `scriptingBackend` (per platform group):
  - `0` = Mono (faster iteration, larger binary, requires runtime JIT —
    forbidden on iOS, WebGL, 微信/抖音小游戏)
  - `1` = IL2CPP (AOT compiled, required for the platforms above)
- `apiCompatibilityLevel`:
  - `3` = .NET Standard 2.1 (default; safer for cross-platform)
  - `6` = .NET Framework (broader BCL, but more libs to strip on IL2CPP)
- `bundleVersion`, `companyName`, `productName`, icons — sanity-check
  before any build pre-flight.

If `scriptingBackend = IL2CPP`, remember:

- Reflection-heavy code (Newtonsoft.Json default settings, custom
  `Activator.CreateInstance`) needs a `link.xml` to survive code
  stripping.
- Generic virtual methods on value types may need explicit AOT hints.

## 5. `ProjectSettings/EditorSettings.asset` — Domain Reload & Serialization

- `m_SerializationMode: 2` (Force Text) → required. If it's `1` (Mixed) or
  `0` (Force Binary), prefabs / scenes can't be reviewed in diffs.
- `m_EnterPlayModeOptionsEnabled: 1` together with
  `m_EnterPlayModeOptions:` containing the `DisableDomainReload` /
  `DisableSceneReload` flags → **static fields will NOT reset between Play
  Mode sessions.** Every static singleton, every `EventBus`, every cached
  delegate MUST use `[RuntimeInitializeOnLoadMethod(SubsystemRegistration)]`
  to reset itself. The provided templates already do this.

## 6. Project root layout — does `Assets/_Project/` exist?

If the canonical layout (see `project-structure.md`) is missing:

- A small/jam project: propose running
  `python3 scripts/init_unity_project_structure.py --path <Assets>` and
  wait for confirmation. Do not auto-create folders.
- An existing project that uses a different layout: **adopt the user's
  layout.** Do not silently migrate files.

Also check for the user's custom context files in the **workspace root**
(not just Assets):

- `GDD.md` / `游戏设计文档.md` → read it before designing systems.
- `H5-Demo/` or any existing prototype → reuse data structures, level
  layouts, scoring rules. Don't reinvent.
- `README.md` / `CONTRIBUTING.md` → may pin a coding style or framework
  choice that overrides this skill's defaults.

## Quick discovery script (recommended)

When the project is large, batch the reads in parallel:

```text
read_file: Packages/manifest.json
read_file: ProjectSettings/ProjectVersion.txt
read_file: ProjectSettings/GraphicsSettings.asset
read_file: ProjectSettings/ProjectSettings.asset
read_file: ProjectSettings/EditorSettings.asset
list_dir: Assets/_Project        (or whatever root the user uses)
```

Summarise findings to the user in **one** short paragraph before writing
code: Unity version, render pipeline, input system, scripting backend,
domain reload state, layout root. Then proceed.
