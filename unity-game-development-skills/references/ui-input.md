# UI & Input

## UI Responsibility Boundary

UI is allowed to:

- Display score / health / timer
- Show buttons and popups
- Forward user clicks via events

UI is NOT allowed to:

- Contain gameplay rules inside `Button.onClick`
- Reach into the gameplay model and mutate it
- Call `FindObjectOfType<GameManager>()` to drive logic

Pattern: UI raises an event or calls a thin façade method (`gameManager.RequestRestart()`); the system owns the rule.

## Recommended Hierarchy

```text
Canvas
  SafeArea
    HUD
      ScoreText
      HealthBar
      TimerText
    Panels
      StartPanel
      WinPanel
      LosePanel
      PausePanel
```

Recommended scripts:

- `HUDView` (binds to gameplay events, updates labels)
- `StartPanel` / `ResultPanel` / `PausePanel` (show/hide, forward clicks)
- `UIManager` (panel stack, transitions)

A drop-in `HUDView` template is at `assets/templates/HUDView.cs.txt`.

## SafeArea

For mobile and 小游戏 builds, wrap HUD/Panels in a SafeArea node that adapts to `Screen.safeArea`. Don't bake notch offsets into individual prefabs.

## Input

### Legacy Input (small/quick demo)

```csharp
Input.GetMouseButtonDown(0)
Input.GetKeyDown(KeyCode.Space)
Input.GetAxisRaw("Horizontal")
```

Acceptable for a 30-minute demo or jam prototype.

### New Input System (production)

When `com.unity.inputsystem` is in `Packages/manifest.json`, use it consistently. Do NOT mix.

Layered structure:

```text
.inputactions asset      (data: action maps, bindings, control schemes)
        ↓ generates C# class via "Generate C# Class"
GameInput (generated)     (typed wrapper, IGameplayActions / IUIActions)
        ↓ implemented by
InputReader (ScriptableObject)   exposes events: MoveEvent, JumpPressedEvent, ...
        ↓ subscribed by
PlayerController, UIManager, CameraRig
        ↓ drives
PlayerMovement / PlayerInteraction / panel transitions
```

A drop-in `InputReader` ScriptableObject template is at
`assets/templates/InputReader.cs.txt`. The SO approach is the official
Unity OpenProject pattern: any system can `[SerializeField]` the same
InputReader asset without scene-coupled lookups.

Do NOT scatter `playerInput.actions["Move"].ReadValue<Vector2>()` calls
across MonoBehaviours — that re-couples gameplay to the binding layer.

## UI Toolkit vs uGUI

Unity 6 ships two runtime UI stacks. Default for casual / 小游戏 work is
**uGUI** (Canvas + RectTransform + TMP):

- Mature ecosystem, every tween library and asset-store package targets it.
- Predictable performance on low-end mobile / 小游戏 runtimes.
- Easy to reference from the Inspector — the workflow this skill assumes.

Reach for **UI Toolkit** (UIElements) only when:

- You need editor-style tooling, large data tables, or complex layout
  rules (flex, grid) that uGUI handles awkwardly.
- The project is a tool, level editor, or in-game console.

Rules of engagement:

- Do **not** mix uGUI and UI Toolkit on the same screen — you'll fight
  two input systems and two layout solvers.
- Do **not** introduce UI Toolkit unsolicited; it changes the entire UI
  authoring workflow.

### Choosing

Before writing input code, check `Packages/manifest.json`:

- Found `"com.unity.inputsystem"` → use Input System
- Not found → use legacy Input (or ask the user before adding the package)

Never add the Input System package to a project unsolicited — it requires `Active Input Handling` changes that restart the editor.

## UI Events

```csharp
public class StartPanel : MonoBehaviour
{
    [SerializeField] private Button startButton;

    public event Action OnStartClicked;

    private void Awake()
    {
        startButton.onClick.AddListener(() => OnStartClicked?.Invoke());
    }
}
```

`GameManager` subscribes to `OnStartClicked` and calls `StartGame()`. The button itself does not contain `StartGame()` logic.
