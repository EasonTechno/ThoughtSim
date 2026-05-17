# 🧠 ThoughtSim - 思维模拟器

[![GitHub Stars](https://img.shields.io/github/stars/EasonTechno/ThoughtSim?style=social)](https://github.com/EasonTechno/ThoughtSim/stargazers)
[![PyPI](https://img.shields.io/pypi/v/thoughtsim)](https://pypi.org/project/thoughtsim/)
[![License](https://img.shields.io/github/license/EasonTechno/ThoughtSim)](LICENSE)

> **用神经网络模拟人类的语言认知与思维模式。**

---

## 🎯 项目简介

ThoughtSim 是从 **MetaLang（共语论）** 项目中独立出来的**思维模拟核心引擎**。

它基于**萨丕尔-沃尔夫假说（语言相对论）**，用神经网络验证一个激进的假设：
> **你用什么语言思考，决定了你有多聪明。**

这个库提供了可复用的组件来：
- 模拟母语锚定效应
- 训练独立的语言子网络
- 探针思维模式的激活模式
- 量化评估不同语言的认知表现

---

## ✨ 核心特性

### 🔗 母语锚定模拟
- 模拟母语在神经网络中建立的深层语义空间
- 验证母语对后续语言学习的"引力效应"
- 可配置的冻结层和稳定性参数

### 🧪 子网络隔离训练
- 创新的正交损失函数设计
- 训练独立于母语的语言思考通路
- 可调节的独立性目标和训练参数

### 🔬 思维模式探针
- 分析不同语言的激活模式区域
- 量化概念表征的差异
- 可视化注意力热力图

### 📊 认知表现评估
- 跨语言对比实验框架
- 多维度认知能力指标
- 递归深度鲁棒性测试

---

## 🚀 快速开始

### 安装

```bash
pip install thoughtsim
```

### 基础用法

```python
from thoughtsim import ThoughtSimulator

# 初始化模拟器，设置母语
sim = ThoughtSimulator(native_language="Chinese")

# 锚定母语网络（模拟母语建立的语义空间）
sim.anchor_native_network(corpus_size=10000)

# 训练英文子网络，目标正交度 70%
result = sim.train_subnetwork(
    language="English",
    orthogonality_target=0.7,
    epochs=100
)

print(f"子网络独立性: {result['final_independence']:.1%}")
print(f"任务准确率: {result['final_accuracy']:.1%}")
```

### 评估认知表现

```python
# 训练多种语言的子网络
sim.train_subnetwork("English", 0.7)
sim.train_subnetwork("StateTransition", 0.85)

# 跨语言评估
df = sim.evaluate_cognitive_performance(
    languages=["Chinese", "English", "StateTransition"],
    task_types=["logical_reasoning", "recursion", "math", "causal_inference"]
)

print(df)
```

### 思维模式探针

```python
# 探针中文的思维模式
cn_pattern = sim.probe_thought_pattern("Chinese", task_type="recursion")
print(f"中文激活区域: {cn_pattern['activation_region']}")

# 探针英文的思维模式
en_pattern = sim.probe_thought_pattern("English", task_type="recursion")
print(f"英文与母语正交度: {en_pattern['orthogonality_to_native']:.1%}")
```

---

## 📁 项目结构

```
ThoughtSim/
├── 📄 thoughtsim.py              # 核心模拟器类（主入口）
├── 📄 requirements.txt           # 依赖
├── 📄 README.md                  # 本文档
├── 📂 native_language_anchored_network/  # 母语锚定网络实现
│   └── 📄 __init__.py
├── 📂 language_cognition/        # 语言认知模块
│   └── 📄 __init__.py
├── 📂 data_models/               # 数据模型
│   └── 📄 __init__.py
├── 📂 task_design/               # 任务设计工具
│   └── 📄 __init__.py
└── 📂 analysis_tools/            # 分析工具
    └── 📄 __init__.py
```

---

## 🔬 核心理论

### 正交损失函数

子网络隔离训练的核心创新：

```math
\mathcal{L}_{total} = \mathcal{L}_{task} + \lambda \cdot \mathcal{L}_{ortho}
```

其中正交损失：

```math
\mathcal{L}_{ortho} = \| A_{cn}^T A_{en} \|_F^2
```

- `A_cn` = 中文注意力头的激活模式
- `A_en` = 英文注意力头的激活模式

目标：让两个矩阵的内积尽量小，也就是激活模式尽量正交。

### 关键发现

1. **母语引力**：先学习的语言会把后学习语言的语义空间"拉过去"
2. **双语优势**：同时学习两种语言可以发展出相对独立的空间
3. **语言专长**：不同语言在不同认知任务上有天然优势
4. **递归突破**：状态转移语言在深度递归任务上表现出惊人鲁棒性

---

## 🤝 与 MetaLang 的关系

```
┌─────────────────────────────────────────────────────────┐
│                     MetaLang（共语论）                    │
│  完整的研究平台 + 人类训练工具 + Web 交互界面              │
└──────────────────────┬──────────────────────────────────┘
                       │  调用
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    ThoughtSim（思维模拟器）               │
│  核心神经网络模拟引擎 + 可复用的实验库                     │
└─────────────────────────────────────────────────────────┘
```

- **ThoughtSim**: 专注于思维模拟的核心算法，可独立安装使用
- **MetaLang**: 完整的研究平台，包含人类训练工具和 Web 界面，依赖 ThoughtSim

---

## 🤝 参与贡献

欢迎所有人加入这个探索人类认知本质的项目！

我们目前需要：
- 🧪 更多思维模式的模拟验证
- 📊 评估指标的设计与优化
- 📝 实验文档和教程
- 🌍 多语言支持

---

## 📬 联系

- **GitHub**: [EasonTechno/ThoughtSim](https://github.com/EasonTechno/ThoughtSim)
- **邮箱**: uu13652153631@qq.com
- **维护者**: [@EasonTechno](https://github.com/EasonTechno)

---

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">
    <strong>🌟 如果这个项目让你眼前一亮，点个Star让更多人看到！🌟</strong>
    <br>
    <sub>用代码探索思维的边界</sub>
</div>