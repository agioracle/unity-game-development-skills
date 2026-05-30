# Unity Game Development Skills

[English](README.md) | 简体中文

AI Agent Skill for building, refactoring, reviewing, and shipping Unity games.

本仓库提供一套面向 AI Agent 的 Unity 游戏开发技能包，包含开发流程、项目规范、检查清单、常用代码模板和辅助脚本。它不是一个可直接用 Unity Editor 打开的 Unity 工程，而是用于指导 Agent 在真实 Unity 项目中更可靠地完成开发任务的 Skills。

## 适用场景

当任务涉及以下内容时，可以使用本 Skill：

- 创建、修改或调试 Unity 游戏项目
- 编写 `MonoBehaviour`、`ScriptableObject`、Prefab、Scene、UI、输入和玩法系统
- 搭建最小可玩闭环、关卡流程、GameManager、对象池、事件总线等基础架构
- 处理 Addressables、存档、本地化、TextMeshPro、Input System 等 Unity 常见模块
- 面向 PC、移动端、WebGL、微信小游戏、抖音小游戏等平台做性能和构建适配
- 对 Unity 项目做结构整理、代码审查、性能优化或交付前检查

## Skill 目录

当前 Skill 目录名为：

```text
unity-game-development-skills
```

## 仓库结构

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

| 路径 | 说明 |
| --- | --- |
| `unity-game-development-skills/SKILL.md` | Skill 主入口，定义触发场景、工作原则、标准流程和交付格式。 |
| `unity-game-development-skills/references/` | Unity 开发规范、平台约束、检查清单和专项指南。 |
| `unity-game-development-skills/assets/templates/` | 可复制到 Unity 项目中的 C# / XML 模板，文件以 `.txt` 保存以避免被误编译。 |
| `unity-game-development-skills/scripts/` | 辅助脚本，目前包含 Unity 项目目录结构初始化脚本。 |
| `LICENSE` | MIT License。 |

## 安装方式

将整个 Skill 目录复制到你的 Agent skills 目录中：

```text
unity-game-development-skills/
```

入口文件是：

```text
unity-game-development-skills/SKILL.md
```

不同 Agent 的 skills 安装目录可能不同，请按所使用工具的 Skill 安装说明放置该目录。

## 推荐工作流

`SKILL.md` 定义了处理 Unity 任务时的标准流程：

1. **Discover**：先读取项目状态，包括 Unity 版本、Packages、ProjectSettings、渲染管线、输入系统和现有目录结构。
2. **Plan**：先规划最小可玩闭环和需要改动的文件，避免过度重构。
3. **Implement**：按编码规范、玩法模式、UI 输入、数据配置和平台性能要求实现。
4. **Verify**：按交付清单自检，确保代码可编译、可验证、可继续迭代。
5. **Report**：交付时说明完成内容、文件变更、Unity 中需要操作、验证方式和注意事项。

## 参考文档

| 文档 | 内容 |
| --- | --- |
| `unity-game-development-skills/references/discovery-checklist.md` | Unity 任务开始前的项目发现清单。 |
| `unity-game-development-skills/references/project-structure.md` | 推荐的 `Assets/_Project/` 目录结构、命名和 asmdef 放置规则。 |
| `unity-game-development-skills/references/coding-standards.md` | C#、`MonoBehaviour`、生命周期、事件订阅和 Domain Reload 相关规范。 |
| `unity-game-development-skills/references/gameplay-patterns.md` | GameManager、关卡、对象池、Prefab、场景职责等玩法架构模式。 |
| `unity-game-development-skills/references/ui-input.md` | UI 层职责、Canvas 层级、Safe Area、新旧输入系统使用建议。 |
| `unity-game-development-skills/references/data-config.md` | `ScriptableObject` 配置、运行时数据、Addressables、存档和本地化规范。 |
| `unity-game-development-skills/references/performance-platform.md` | Update 热路径、GC、对象池、移动端、WebGL、小游戏平台和 IL2CPP 裁剪注意事项。 |
| `unity-game-development-skills/references/delivery-checklist.md` | 交付前检查项、回复格式和 Unity 任务硬性禁忌。 |

## 代码模板

模板位于：

```text
unity-game-development-skills/assets/templates/
```

| 模板 | 建议复制到 Unity 项目的位置 | 用途 |
| --- | --- | --- |
| `EventBus.cs.txt` | `Assets/_Project/Code/Runtime/Core/EventBus.cs` | 类型安全事件总线。 |
| `GameManager.cs.txt` | `Assets/_Project/Code/Runtime/Core/GameManager.cs` | 基础游戏状态机。 |
| `HUDView.cs.txt` | `Assets/_Project/Code/Runtime/UI/HUDView.cs` | HUD 表现层模板。 |
| `InputReader.cs.txt` | `Assets/_Project/Code/Runtime/Input/InputReader.cs` | 新 Input System 输入读取器模板。 |
| `MonoSingleton.cs.txt` | `Assets/_Project/Code/Runtime/Core/MonoSingleton.cs` | 泛型 `MonoBehaviour` 单例基类。 |
| `SimpleObjectPool.cs.txt` | `Assets/_Project/Code/Runtime/Systems/SimpleObjectPool.cs` | 简单对象池实现。 |
| `link.xml.txt` | `Assets/link.xml` | IL2CPP / Managed Code Stripping 保留配置模板。 |

使用模板时请注意：

- 复制到 Unity 项目后需要去掉 `.txt` 后缀。
- 按目标项目修改 namespace、程序集和依赖。
- 不要把整个 Skill 仓库直接拖入 Unity 项目作为可编译代码。
- `InputReader.cs.txt` 依赖 Unity 新 Input System，并假设已生成 `GameInput` C# 类。
- `HUDView.cs.txt` 使用 TextMeshPro，即 `TMPro` 命名空间。

## 初始化 Unity 项目目录结构

可以使用脚本为目标 Unity 项目的 `Assets` 目录创建推荐结构：

```bash
python3 unity-game-development-skills/scripts/init_unity_project_structure.py --path /absolute/path/to/UnityProject/Assets
```

脚本默认会在 `Assets` 下创建 `_Project` 目录骨架和 `.gitkeep` 文件，不会创建脚本、场景或 Prefab，也不会修改 `Packages`、`ProjectSettings` 或已有文件。

可选参数：

```bash
# 指定项目资源根目录名
python3 unity-game-development-skills/scripts/init_unity_project_structure.py --path /absolute/path/to/UnityProject/Assets --root MyProject

# 显式创建 Resources 目录
python3 unity-game-development-skills/scripts/init_unity_project_structure.py --path /absolute/path/to/UnityProject/Assets --with-resources

# 不创建 .gitkeep
python3 unity-game-development-skills/scripts/init_unity_project_structure.py --path /absolute/path/to/UnityProject/Assets --no-gitkeep
```

推荐目录结构示例：

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

默认不创建 `Resources/`，如确有需要请使用 `--with-resources`。

## Unity 项目使用建议

- 修改前先确认 Unity 版本、渲染管线、输入系统、脚本后端和平台目标。
- 优先实现最小可玩闭环，再扩展表现、关卡、资源和平台适配。
- 运行时热路径避免频繁 `FindObjectOfType`、`GetComponent`、LINQ、装箱和临时分配。
- `MonoBehaviour` 尽量只作为 Unity 胶水层，核心业务逻辑优先拆到纯 C# 类。
- `ScriptableObject` 适合作为静态配置，运行时状态应拆到 runtime model。
- 面向 IL2CPP、WebGL 或小游戏平台时，注意代码裁剪、文件系统、音频解锁、内存峰值和异步加载限制。

## 许可证

本项目使用 [MIT License](LICENSE)。
