# g1_style_learning

基于 Unitree G1 的风格化学习和地形适应算法实践，使用 Isaac Lab 的 ManagerBased 工作流。

当前已完成官方 G1 29DoF rev_1_0 本地资产接入、关节位置控制与零动作环境检查。策略动作维度为 29，当前 policy 观测维度为 93。项目尚未实现 AMP 或完成行走策略训练，也尚未完成实机部署验证。

## 环境

当前开发环境使用 Isaac Sim 6.0、Isaac Lab 3.0 和 Python 3.12。请先激活能够运行 Isaac Lab 的 Python 环境。

## 目录

```text
g1_style_learning/
├── scripts/                         # 零动作检查与训练、评估入口
└── source/g1_style_learning/
    ├── config/                      # 扩展元数据
    └── g1_style_learning/
        ├── assets/
        │   ├── g1.py                # 机器人资产与执行器配置
        │   └── robots/
        │       └── g1_29dof_rev_1_0/ # USD 及 configuration 配套资源
        └── tasks/manager_based/g1_style_learning/
            ├── g1_style_learning_env_cfg.py
            ├── agents/              # 训练算法配置
            └── mdp/                 # 自定义 MDP 函数
```

## 模型资源

模型配置从 `g1.py` 所在目录定位 `robots/g1_29dof_rev_1_0/g1_29dof_rev_1_0.usd`，不依赖用户名或终端工作目录。必须保留 USD 配套文件的相对目录结构；LFS 文件应下载为真实资产，不能只保留指针文本。

模型来源为宇树官方 [unitree_model](https://huggingface.co/datasets/unitreerobotics/unitree_model)，配置参考 [unitree_rl_lab](https://github.com/unitreerobotics/unitree_rl_lab)。

## 运行检查

列出任务：

```bash
python scripts/list_envs.py
```

运行单环境零动作检查：

```bash
python scripts/zero_agent.py --task Template-G1-Style-Learning-v0 --num_envs 1
```

当前动作是相对默认关节位置的偏移，缩放为 0.1。零动作让执行器跟踪默认关节姿态，不包含主动平衡控制，也不保证机器人持续站稳。当前奖励仅为环境检查占位，不应直接用于行走训练。

## 开发方向

先建立速度指令跟踪的 PPO 基线，再接入参考动作数据与 AMP，后续扩展台阶和平台任务。机器人资产、环境配置、自定义 MDP 函数和训练算法配置分别管理。

## 许可与来源

仓库的 LICENSE 不自动覆盖第三方资产及代码。Isaac Lab 模板保留原始许可标头；宇树模型及其他第三方资源按其来源的许可条款使用和分发。
