# Gameplay Patterns

## Implementation Order

When creating a new gameplay feature, answer these in order:

1. Game goal
2. Player operations
3. Core objects
4. State changes
5. Win condition
6. Lose condition
7. Feedback presentation
8. Restart flow

Every gameplay script must answer:

- What is this system responsible for?
- What does it depend on?
- What events does it expose?
- How is it initialized?
- How is it reset?
- How is it tested / verified?

## Recommended Base Architecture (small/medium casual games)

```text
GameManager          State machine: Ready/Playing/Paused/Win/Lose, restart flow
LevelManager         Load level, build scene objects, tear down
InputManager / InputReader   Input abstraction
UIManager            HUD + popups
AudioManager         BGM / SFX
PoolManager          Object pools
SaveManager          Local save
EventBus (optional)  Cross-system events
```

Do NOT introduce a heavy framework (Zenject/UniRx/ECS) for a small demo unless explicitly requested.

## Game State Machine

```csharp
public enum GameState
{
    None,
    Ready,
    Playing,
    Paused,
    Win,
    Lose,
}

public event Action<GameState> OnGameStateChanged;

public void ChangeState(GameState newState)
{
    if (currentState == newState) return;
    currentState = newState;
    OnGameStateChanged?.Invoke(currentState);
}
```

State transitions live in `GameManager` only. UI/Audio/VFX subscribe.

## Scene vs Prefab Discipline

A scene should be light. Keep in scene only:

- `GameManager`
- `UI Root` (Canvas)
- `Camera`
- `Light`
- `Level Root` (empty)
- Necessary scene entry points

Everything else is a prefab:

- Player, Enemy, Bullet, Tile, Coin, Obstacle, Popup, Button, Effect

## Self-Contained Prefabs

A prefab must include everything it needs to function:

- Visuals
- Colliders
- Animator (if any)
- Audio source / trigger points
- Its scripts
- Required child node references

A prefab MUST NOT depend on a hidden scene object discovered at runtime.

## Animation

### Use Tween or Coroutine for small feedback

Button scale, coin flying, tile flip, damage number, screen shake, popup intro — these do NOT need an Animator.

On Unity 6, prefer `UnityEngine.Awaitable` for short async feedback over
hand-written coroutines — it composes with `await`, propagates exceptions
naturally, and avoids the IEnumerator allocation:

```csharp
// ✅ Modern: short feedback as awaitable async (Unity 6+)
public async Awaitable FlashAndHide(SpriteRenderer sr)
{
    sr.color = Color.white;
    await Awaitable.WaitForSecondsAsync(0.1f);
    sr.color = Color.red;
    await Awaitable.NextFrameAsync();
    sr.enabled = false;
}

// ✅ Acceptable: tween library (DOTween / PrimeTween) for chained motion
transform.DOPunchScale(Vector3.one * 0.2f, 0.15f);
```

Coroutines are still fine for multi-frame loops where you genuinely need
`yield return`. Use them; just don't reach for them as the default any
more on Unity 6.

### Use Animator for character states

Idle / Run / Attack / Hit / Die / Win / Lose — these belong in an `AnimatorController`.

Do not create one Animator per UI button.

## Physics

### Don't over-use physics

Grid / card / match / click games rarely need `Rigidbody`. Prefer:

- Grid coordinates
- Raycast for picks
- `Collider2D` triggers
- Hand-coded movement

### Separate physics from logic

```csharp
private void OnTriggerEnter(Collider other)
{
    if (other.TryGetComponent(out Coin coin))
    {
        coin.Collect();
    }
}
```

The trigger only notifies. Scoring / SFX / UI update happen elsewhere.

## Object Pooling

For bullets, effects, enemies, floating texts — pool them. A minimal interface:

```csharp
public interface IPoolable
{
    void OnSpawn();
    void OnDespawn();
}
```

A ready-to-use pool template lives at `assets/templates/SimpleObjectPool.cs.txt`.

## Editor Tools

Editor scripts MUST live under `Assets/_Project/Code/Editor/` with their own `.asmdef`. Editor APIs in Runtime code break builds.

## Casual Demo Priority Ladder

```text
P0: Core gameplay playable
P0: Win/Lose conditions
P0: Restart works
P1: Basic UI
P1: Basic SFX
P1: Basic animation feedback
P2: Level configuration
P2: Onboarding
P2: Result screen polish
P3: Skins / shop / progression
P3: Ads / IAP / remote config
```

Never deliver P3 features when P0 is unfinished.
