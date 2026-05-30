# C# & Script Design Standards

## MonoBehaviour Discipline

A `MonoBehaviour` is glue between Unity and game logic. It should ONLY:

- Hold Inspector-serialized configuration (`[SerializeField]`)
- Handle Unity lifecycle (`Awake` / `OnEnable` / `Start` / `Update` / `OnDisable` / `OnDestroy`)
- Receive input events
- Forward calls to pure C# logic
- Drive presentation (transform, animator, particles, UI)

A `MonoBehaviour` should NEVER:

- Contain all the rules of the game
- Run heavy business logic in `Update`
- Use `FindFirstObjectByType` / `GameObject.Find` at runtime hot paths (and never use the now-obsolete `FindObjectOfType`)
- Rely on global mutable static state for game data without resetting it on Play Mode entry (see "Domain Reload Safety" below)

## Split Logic into Pure C# Classes

Boards, paths, scoring, level rules, AI decision trees, math — keep them as plain classes so they can be unit-tested.

```csharp
public class BoardModel
{
    public int Width { get; }
    public int Height { get; }

    public BoardModel(int width, int height)
    {
        Width = width;
        Height = height;
    }

    public bool IsInside(int x, int y)
    {
        return x >= 0 && x < Width && y >= 0 && y < Height;
    }
}
```

A `MonoBehaviour` then owns a `BoardModel` instance and renders it.

## Events for Decoupling

```csharp
public event Action<int> OnScoreChanged;
public event Action OnGameOver;
```

Recommended dependency direction:

```text
GameManager  ── raises events ──▶
                                  UIManager      (refresh UI)
                                  AudioManager   (play SFX)
                                  VFXManager     (play effects)
```

UI never reads game rules directly. Game rules never `GetComponent<Text>()`.

## Cache, Don't Search

```csharp
// ❌ Avoid
private void Update()
{
    var gm = FindFirstObjectByType<GameManager>(); // and never use the obsolete FindObjectOfType
    var rb = GetComponent<Rigidbody>();
    var p  = Camera.main.ScreenToWorldPoint(Input.mousePosition);
}

// ✅ Do
private Camera mainCamera;
private Rigidbody rb;

private void Awake()
{
    mainCamera = Camera.main;        // OK in Awake; Camera.main does a Find internally — never call it in Update
    rb = GetComponent<Rigidbody>();
}
```

### Camera.main caveat (multi-scene / additive)

Cache `Camera.main` in `Awake`, but if your game switches the Main Camera
mid-run (cutscene rig, level transition, additive scene that brings its own
camera), refresh the cache on `SceneManager.sceneLoaded` or expose a
`RefreshMainCamera()` method. A stale `mainCamera` reference is a common
source of "screen-to-world conversions return wrong values" bugs.

## Domain Reload Safety

Unity 6 ships with **Enter Play Mode Options → Disable Domain Reload**
enabled in many starter templates. When disabled, **static fields are NOT
reset** between Play Mode sessions, so the second Play of the editor will
see "ghost" state from the first Play (dead singleton instances, lingering
`EventBus` subscribers, half-initialised caches).

Every static field that holds gameplay state, a singleton reference, or an
event subscription list MUST reset itself on `SubsystemRegistration`:

```csharp
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    private static void ResetStatics()
    {
        Instance = null;
    }

    private void OnDestroy()
    {
        if (Instance == this) Instance = null;
    }
}
```

The same rule applies to `EventBus`, static caches, static event handlers,
and any `[RuntimeInitializeOnLoadMethod]`-driven bootstrap. The provided
`MonoSingleton`, `EventBus`, and `GameManager` templates already follow
this pattern — keep it that way when you adapt them.

## Null-Safety in Generated Scripts

Every generated script that depends on Inspector references must:

- Either have `[SerializeField]` with a clear field name
- And/or guard against null in `Awake`/`Start`:

```csharp
private void Awake()
{
    if (target == null)
    {
        Debug.LogError($"[{nameof(EnemyController)}] target is not assigned.", this);
        enabled = false;
    }
}
```

## Logging Standard

```csharp
Debug.Log("[GameManager] Game started.");
Debug.LogWarning("[LevelLoader] Level config missing.");
Debug.LogError("[AudioManager] Audio source is null.");
```

- Tag every log with the system name in brackets.
- No spam. No leftover `Debug.Log("here")` / `Debug.Log(1)`.
- Errors must include enough context to locate the problem.

## Required Properties of Every Generated Script

1. File name = class name.
2. Namespace consistent with project.
3. Tunables exposed via `[SerializeField]`.
4. Null references protected.
5. Critical sections commented.
6. Compiles against the project's Unity version.
7. Does not depend on a hidden scene object.
8. No Editor-only API in Runtime files.

## Code Smell Checklist

If any of these appear in generated code, fix them before delivery:

- `using UnityEditor;` in a Runtime script
- `GameObject.Find(...)` / `FindFirstObjectByType(...)` / the obsolete `FindObjectOfType(...)` outside `Awake`
- Massive `MonoBehaviour` (> ~300 lines) doing many unrelated things
- `static` mutable game state without a clear lifetime
- Coroutine that never has a stop condition
- `Update` allocating per frame (`new`, `string +`, `ToList`, `ToArray`)
