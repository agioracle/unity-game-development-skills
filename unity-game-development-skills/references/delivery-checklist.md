# Delivery Checklist & Reply Format

## Acceptance Criteria

A Unity feature is NOT complete until ALL of the following are true:

```text
1.  Unity Console has no compile errors.
2.  Core flow runs end-to-end in Play Mode.
3.  No Missing Script / Missing Reference on any used GameObject.
4.  Key parameters are tunable in the Inspector.
5.  Failure paths are guarded (null checks, empty configs, unloaded scenes).
6.  Code style matches the existing project conventions.
7.  The user knows exactly how to verify the feature.
8.  New asset paths are clear and consistent.
9.  No existing functionality has been broken.
10. The result is extendable (open for next feature without rewrite).
```

If any item is uncertain, state it explicitly in the reply — do NOT fake completion.

## 禁忌 (Hard Bans)

Do NOT do any of these unless the user explicitly asked:

```text
1.  Stuff every system into one giant GameManager.
2.  Use `GameObject.Find` / `FindFirstObjectByType` (or the obsolete `FindObjectOfType`) anywhere outside Awake.
3.  `GetComponent` / `FindFirstObjectByType` every frame.
4.  Modify ProjectSettings.
5.  Bump package versions.
6.  Delete user files.
7.  Ship code that does not compile.
8.  Ignore Unity lifecycle (e.g., do work in a constructor).
9.  Place Editor code into Runtime asmdef.
10. Drag in a heavy framework just to write 100 lines of demo logic.
11. Claim "done" without a verification path.
12. Provide only code — ignoring Prefab / Scene / Inspector wiring.
13. Hold mutable state in `static` fields without a `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]` reset — Domain Reload disabled = stale singletons / dictionaries / events leaking across Play sessions. See `coding-standards.md` → "Domain Reload Safety".
```

## Required Reply Format

After completing a Unity task, reply using exactly this Markdown skeleton (translate headings if the conversation is in Chinese — the structure stays the same):

```markdown
## 完成内容

- 新增了 XXX 系统
- 修改了 XXX 脚本
- 新增了 XXX Prefab 配置方式

## 文件变更

- Assets/_Project/Code/Runtime/Gameplay/PlayerController.cs (新增)
- Assets/_Project/Code/Runtime/Core/GameManager.cs (修改)
- Assets/_Project/Configs/ScriptableObjects/SO_Level_001.asset (新增)

## Unity 中需要操作

1. 打开 Assets/_Project/Scenes/Main.unity
2. 将 PlayerController 挂到 Player Prefab 上
3. 在 GameManager 的 Inspector 把 SO_Level_001 拖到 Level Config 字段
4. 点击 Play 测试

## 验证方式

- 点击 Start 按钮进入游戏
- 玩家可以左右移动
- 收集 3 个目标后触发胜利面板
- 生命值降到 0 触发失败面板
- 点击 Restart 可以重开

## 注意事项

- 当前使用临时 Sprite，后续可替换为正式美术
- 对象池和 Addressables 暂未接入（P2）
- 仅在 Editor 验证过；移动端构建尚未测试
```

### Section Rules

- **完成内容**: business-level summary, no file paths.
- **文件变更**: full project-relative paths, mark `(新增)` / `(修改)` / `(删除)`.
- **Unity 中需要操作**: numbered, executable steps a human can follow without reading the code.
- **验证方式**: observable behaviors in Play Mode, not internal state assertions.
- **注意事项**: known limits, deferred work, assumptions made (e.g., "assumed legacy Input").

## Self-Check Before Sending

Run this final mental pass:

1. Does each new `.cs` file have a matching class name and a sensible namespace?
2. Are all `[SerializeField]` references actually wired in the scene/prefab, OR explicitly listed under "Unity 中需要操作"?
3. Are there any `Debug.Log` left for temporary debugging? Remove or downgrade.
4. Any `TODO` comments left in code? Either resolve or surface them in 注意事项.
5. Did the change touch anything outside the agreed scope? If yes, surface it.

Only when all five pass, send the reply.
