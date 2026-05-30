# Data & Configuration

## ScriptableObject for Static Config

Use `ScriptableObject` for designer-tunable static data:

- Level configs
- Character / enemy / item / skill stats
- Audio configs
- Difficulty curves
- Board sizes
- Color palettes

```csharp
[CreateAssetMenu(menuName = "Game/Level Config", fileName = "SO_Level_001")]
public class LevelConfig : ScriptableObject
{
    public int width = 8;
    public int height = 8;
    public int mineCount = 10;
    public int rescueTargetCount = 3;
}
```

Place SO assets under `Assets/_Project/Configs/ScriptableObjects/` or `.../Levels/`.

## Runtime State ≠ Config Asset

ScriptableObject assets are **default configuration** loaded from disk. Mutating them at runtime can leak between play sessions and into source control.

```text
❌ levelConfig.mineCount = 5;     // mutates the asset on disk
✅ runtimeModel = new LevelRuntime(levelConfig);
   runtimeModel.MineCount = 5;
```

Pattern:

```csharp
public class LevelRuntime
{
    public int MineCount;
    public int Score;

    public LevelRuntime(LevelConfig config)
    {
        MineCount = config.mineCount;
        Score = 0;
    }
}
```

`GameManager` holds the `LevelRuntime`; the SO is read-only after `Awake`.

## Asset Loading

### Small demo / prototype

Direct prefab/Sprite/AudioClip references via `[SerializeField]`. Don't introduce Addressables prematurely.

### Mid-to-large project

Use Addressables for:

- Level packs
- Skins / characters
- Large audio
- Remote / DLC content
- Per-platform variant assets

Rules:

- All Addressables loads are async (`LoadAssetAsync`, `InstantiateAsync`).
- Every load must have a matching `Addressables.Release` (or release of the operation handle).
- Do NOT mix `Resources/` and Addressables for the same logical asset bucket.
- Do NOT put every asset in a single Addressables Group — split by feature/platform.

### Anti-pattern: dropping the AsyncOperationHandle

The most common Addressables leak is throwing away the handle and only
keeping the loaded asset. Once the handle is gone, you can no longer
release the asset and reference counting is permanently off.

```csharp
// ❌ Handle is lost the moment the await completes.
//    Addressables.Release(prefab) compiles but does NOT free the asset
//    correctly because Release(TObject) requires the handle.
var prefab = await Addressables.LoadAssetAsync<GameObject>(key).Task;

// ❌ Same problem with InstantiateAsync — Destroy(go) leaves the
//    Addressables refcount alive forever.
var go = await Addressables.InstantiateAsync(key).Task;
Destroy(go);
```

```csharp
// ✅ Hold the handle for the asset's lifetime, release it explicitly.
private AsyncOperationHandle<GameObject> prefabHandle;

public async Awaitable LoadAsync(string key)
{
    prefabHandle = Addressables.LoadAssetAsync<GameObject>(key);
    await prefabHandle.Task;
    if (prefabHandle.Status != AsyncOperationStatus.Succeeded)
    {
        Debug.LogError($"[Addressables] Load failed: {key}");
        return;
    }
    // use prefabHandle.Result ...
}

public void Unload()
{
    if (prefabHandle.IsValid()) Addressables.Release(prefabHandle);
}

// ✅ For instantiated GameObjects, use ReleaseInstance — it both decrements
//    refcount AND destroys the GameObject.
var go = await Addressables.InstantiateAsync(key).Task;
// ... later ...
Addressables.ReleaseInstance(go);   // not Destroy(go)
```

Pair every `LoadAssetAsync` / `InstantiateAsync` with a release point in
`OnDestroy`, scene unload, or your level teardown. Audit at delivery
time — Addressables leaks only show up after the second or third level
load.

Refer to the official manual: <https://docs.unity3d.com/Manual/com.unity.addressables.html>.

## Save / Persistence

Recommend `SaveManager` writing to `Application.persistentDataPath` with a versioned JSON or binary format.

- Always wrap in `try/catch`.
- Include a schema version field so future migrations are possible.
- Never persist runtime references (GameObjects, components) — persist data.

## Localization

If localization is needed and not yet present, ask before adding `com.unity.localization`. Otherwise, use a simple `Dictionary<string,string>` driven by a SO table for the demo.
