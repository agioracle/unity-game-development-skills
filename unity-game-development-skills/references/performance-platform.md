# Performance & Multi-Platform

## Update Hygiene

Avoid in `Update` / `LateUpdate` / `FixedUpdate`:

- `FindFirstObjectByType` / `FindAnyObjectByType` / `GameObject.Find` (and the now-obsolete `FindObjectOfType`)
- `GetComponent` on the same object every frame
- `Camera.main` (it does a Find under the hood)
- `new` allocations, `string +` concatenation, LINQ (`Where`, `Select`, `ToList`)
- Boxing (passing `int` to `object`-taking methods)
- Unboxed event invocations in tight loops

Do instead:

- Cache references in `Awake`.
- Use `StringBuilder` or pre-formatted strings for HUD text.
- Use plain `for` over `foreach` on `List<T>` in hot paths if profiler shows allocations.

## Pooling

Frequent `Instantiate` / `Destroy` (bullets, hits, floating numbers, FX, enemies) MUST go through a pool. See `assets/templates/SimpleObjectPool.cs.txt`.

## Mobile Constraints

```text
- Reduce overdraw / transparent overlap
- Control draw calls (atlas sprites, batch UI)
- Avoid huge textures; use platform-appropriate compression (ASTC for iOS/Android)
- Compress audio (Vorbis for music, ADPCM for short SFX)
- Minimize realtime lights and shadows
- Reduce post-processing
- Avoid over-using Animator on UI
- Avoid per-frame GC allocations
- Control first-pack size
```

## WebGL Constraints

```text
- First-pack size matters; strip unused code, use code stripping level "High"
- Avoid huge runtime memory footprint (browsers cap memory)
- All asset loading should be async; do NOT block on sync I/O
- Mind browser API compatibility (no System.IO.File for arbitrary paths)
- Do NOT use threads except via Web Workers / Unity-supported APIs
- Test on Chrome AND Safari (audio policies differ)
```

## 微信小游戏 / 抖音小游戏 Constraints

Highest pressure on size and runtime memory.

```text
- Strict 首包 size limits — must use 分包 (subpackages)
- Texture sizes capped; mind GPU memory peaks
- Runtime memory peaks cause OOM kills on low-end devices
- Platform APIs differ from standard WebGL (login, share, payment, file system, network)
- Some Unity APIs are unsupported or behave differently
- Audio: prefer the platform's audio API for BGM if Unity audio is too heavy
- Save to platform's storage API, not arbitrary file paths
```

### Real-world traps that will brick a 小游戏 build

These are not theoretical — every one of them has shipped a broken build
to production. Apply them defensively from day one.

1. **Single-threaded runtime — `Task.Run` does NOT help.**
   WebGL / 微信小游戏 / 抖音小游戏 run in a single JS-thread sandbox.
   `System.Threading.Tasks.Task.Run(() => Heavy())` will execute
   **synchronously on the main thread** and stall the frame. For
   off-main-thread feel, use:
   - `UnityEngine.Awaitable` (Unity 6) for frame-yielding async
   - Coroutines yielding `null` / `WaitForSeconds`
   - Slice heavy work across frames manually (`for (...; deadline)`)

2. **Reflection + IL2CPP code stripping eats your types.**
   Default Newtonsoft.Json (`Json.NET`) deserialization fails at runtime
   on 小游戏 builds because the target types were stripped. Mitigations:
   - Prefer `System.Text.Json` (Unity 6 ships a runtime-friendly subset)
     or hand-written serializers.
   - If you must use Newtonsoft, add a `link.xml` listing the types to
     preserve, and verify on-device. See template
     `assets/templates/link.xml.txt` (copy to `Assets/link.xml` and fill in
     your namespaces).
   - Same applies to `Activator.CreateInstance<T>()`, generic value-type
     delegates, and `[Serializable]` types loaded only via reflection.

3. **AudioSource.Play before user interaction = silence.**
   Browsers (and 小游戏 runtimes that wrap them) block audio until the
   first user gesture. Don't auto-play BGM in `Awake`/`Start` of the Boot
   scene; queue it from the first tap on the start button. Provide an
   "audio unlocked" event so dependent systems (voice-over, tutorial)
   wait for it.

4. **PlayerPrefs is small, async-flushed, and platform-quirky.**
   - 微信小游戏: backed by `wx.setStorage`, ~10 MB total quota for the
     whole mini-game; individual keys further capped.
   - WebGL: backed by IndexedDB, written **asynchronously**. Reading the
     key you just wrote in the same frame may return the old value.
   - Always `PlayerPrefs.Save()` after a batch of writes, and budget for
     it failing on quota-full devices. For anything > a few KB, use the
     platform's storage API directly behind an interface, not PlayerPrefs.

5. **Avoid `System.IO.File` on arbitrary paths.**
   Only `Application.persistentDataPath` is writable, and on 小游戏 it
   maps to a sandbox. `StreamingAssets` reads must use `UnityWebRequest`
   on WebGL/小游戏 — direct `File.ReadAllBytes` will fail.

6. **Mind first-frame memory peak.**
   Unity loads the scene + all referenced assets before the first frame.
   On 1 GB devices this peaks dangerously high. Keep the Boot scene
   minimal and load gameplay assets via Addressables / additive scenes.

When generating code that targets these platforms:

- Wrap platform-specific calls behind an interface so they can be stubbed in Editor.
- Use `#if UNITY_WEBGL && !UNITY_EDITOR` for platform-only branches.
- Confirm with the user which adapter SDK is in use (e.g., 微信小游戏 转换工具 / WX-WASM-SDK / Bytedance Tools) before assuming APIs.

## Build Pre-Flight Checklist

Before declaring a build-ready state:

```text
[ ] Build Target matches the intended platform
[ ] Scenes In Build are correct and ordered (Boot → Menu → Game)
[ ] Console has zero errors and zero red warnings
[ ] No "Missing Script" or "Missing Reference" anywhere
[ ] No `using UnityEditor` in Runtime asmdefs
[ ] No `Resources/` abuse
[ ] No uncompressed huge textures
[ ] Test/debug GameObjects removed or disabled
[ ] Player Settings (icon, name, bundle id) reasonable for the target
```

Reference: <https://docs.unity3d.com/6000.3/Documentation/Manual/best-practice-guides.html>

## Profiling Quick Tips

- Always profile on the **target device**, not the Editor, for mobile/WebGL/小游戏 work.
- Watch GC.Alloc per frame in the Profiler — target 0 in steady state.
- Use the Memory Profiler package for snapshots; compare before/after a level transition for leaks.
- For draw calls, enable Frame Debugger; collapse static UI under a single Canvas where possible.
