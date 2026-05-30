# Project Structure & Naming

## Canonical Layout

Place all project-specific assets under `Assets/_Project/`. Third-party plugins stay outside `_Project`.

```text
Assets/
  _Project/
    Art/
      Sprites/
      Models/
      Materials/
      Animations/
      Fonts/
      VFX/
    Audio/
      BGM/
      SFX/
    Code/
      Runtime/
        Core/
        Gameplay/
        UI/
        Systems/
        Data/
        Utils/
      Editor/
      Tests/
    Configs/
      ScriptableObjects/
      Levels/
    Prefabs/
      Characters/
      Gameplay/
      UI/
      Effects/
    Scenes/
      Boot.unity
      Menu.unity
      Game.unity
    Addressables/
    StreamingAssets/
```

> `Resources/` is intentionally **omitted** from the canonical default.
> Add it only when the project genuinely needs always-loaded global data
> (e.g., a single bootstrap config). For everything else, use
> Addressables. The `init_unity_project_structure.py` script honours this
> rule via the explicit `--with-resources` flag.

## Layout Rules

1. All project assets live under `Assets/_Project`.
2. Third-party plugins are NEVER moved into `_Project`.
3. Runtime code and Editor code are physically separated; each has its own `*.asmdef`.
4. Prefabs, Scenes, Configs, and Art never live in the same folder.
5. Test scenes are separated from shipping scenes.
6. `Resources/` is reserved for tiny, always-loaded data; prefer Addressables for everything else.

## Assembly Definitions

Recommended `.asmdef` placement:

- `Assets/_Project/Code/Runtime/Project.Runtime.asmdef`
- `Assets/_Project/Code/Editor/Project.Editor.asmdef` (with `Editor` as the only included platform, references `Project.Runtime`)
- `Assets/_Project/Code/Tests/EditMode/Project.Tests.EditMode.asmdef` (Editor platform only, references `Project.Runtime` + nunit)
- `Assets/_Project/Code/Tests/PlayMode/Project.Tests.PlayMode.asmdef` (all platforms, references `Project.Runtime` + nunit + Test Framework)

This prevents Editor APIs from leaking into Runtime builds, and keeps
EditMode tests from accidentally pulling Editor-only symbols into a
PlayMode test run.

## Testing Layout

Unity's Test Framework supports two test categories — they are NOT
interchangeable.

| | EditMode | PlayMode |
|---|---|---|
| Runs in | Editor process, no scene loop | Real PlayMode loop with `Update`/`FixedUpdate` |
| Speed | Fast (milliseconds) | Slower (seconds), spins up runtime |
| Use for | Pure C# models (Board, Scoring, Pathfinding, RNG, save format) | MonoBehaviour behaviour, coroutines, physics, scene wiring |
| Asmdef platform | Editor only | All platforms (so it can also run in built players) |

Rules of thumb:

- **Pure C# logic must be testable in EditMode.** If a class needs
  `MonoBehaviour` to be tested, it has too much glue and should be split
  into a model + a thin `MonoBehaviour` wrapper (see
  `coding-standards.md` → "Split Logic into Pure C# Classes").
- **PlayMode tests are for behaviour, not algorithm correctness.** Assert
  things like "after 3 frames the bullet pool reused 3 instances", not
  "1 + 1 == 2".
- Tests follow the production naming convention:
  `BoardModelTests.cs` next to the asmdef, with `[Test]` /
  `[UnityTest]` methods named `MethodUnderTest_Scenario_Expected`.

A minimal EditMode test:

```csharp
using NUnit.Framework;
using Project.Gameplay;

namespace Project.Tests.EditMode
{
    public class BoardModelTests
    {
        [Test]
        public void IsInside_OutOfBounds_ReturnsFalse()
        {
            var board = new BoardModel(8, 8);
            Assert.IsFalse(board.IsInside(-1, 0));
            Assert.IsFalse(board.IsInside(8, 0));
        }
    }
}
```

## File Naming

| Asset | Convention | Example |
|---|---|---|
| Script | `PascalCase.cs` (file name MUST match class name) | `PlayerController.cs` |
| Prefab | `PascalCase.prefab` | `Player.prefab` |
| Scene | `PascalCase.unity` | `Main.unity` |
| Material | `M_*.mat` | `M_Player.mat` |
| Sprite | `S_<Category>_<Name>.png` | `S_Icon_Coin.png` |
| AnimationClip | `A_<Subject>_<Action>.anim` | `A_Player_Run.anim` |
| AnimatorController | `AC_*.controller` | `AC_Player.controller` |
| ScriptableObject asset | `SO_<Type>_<Variant>.asset` | `SO_Level_001.asset` |
| Audio | `SFX_*.wav` / `BGM_*.wav` | `SFX_Click.wav` |

## C# Naming

```csharp
public class PlayerController : MonoBehaviour
{
    [SerializeField] private float moveSpeed = 5f;

    private int currentHealth;

    public int CurrentHealth => currentHealth;

    private void Awake() { }
    private void Start() { }
    private void Update() { }

    public void TakeDamage(int damage) { }
}
```

| Symbol | Convention |
|---|---|
| Class / Struct / Enum | `PascalCase` |
| Method | `PascalCase` |
| `public` property | `PascalCase` |
| `private` field | `camelCase` |
| `[SerializeField] private` field | `camelCase` |
| Constant | `PascalCase` or `UPPER_CASE` (project-consistent) |
| Interface | `IInteractable` |
| Event | `OnHealthChanged` |
| Namespace | `Project.Gameplay`, `Project.UI`, ... |

## When the project does not match this layout

Do NOT silently migrate. Either:

1. Adopt the user's existing layout and write all new files into it consistently, or
2. Propose the canonical layout, list which files would move, wait for explicit confirmation.
