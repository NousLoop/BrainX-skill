# BrainMass 外层复核

## 证据与复现

在 Windows Git Bash 通过 Docker 以归档镜像 ID `sha256:8cc3d09f69ae914034abf22e0bcd10db36f8344588ad0b691062454ebff648cf` 运行。容器断网，只读挂载本次实验归档，在容器临时目录复制项目后执行 README 中的 `test_checks.py`、正式参数复跑及诊断绘图。指定 CPU、Agg 后端和可写的 `MPLCONFIGDIR`，以便复核先前受只读缓存限制的测试。外层复核未调用模型。

- 单元检查通过，包括导数与单步检查、状态重置和时间坐标、标量与原生批处理一致性、JIT 一致性、滤波、替代序列与观测配对检查。
- `launch.py production-replay production_exact_config.json` 退出 0，生成三组诊断图，各有 PNG 和 PDF。另目视检查了已归档的三张最终 PNG，条件、轴和图例可辨，扫描图标出了基线不满足 gamma 判据的网格点。
- 对正式运行和复跑的 7 个 NPZ 逐字段核对键、形状和 dtype。两个 `elapsed_s` 字段随运行变化，其余 77 个数组相同，所有有限浮点值的最大绝对差为 0，离散结果逐元素相同。`assess_results.py` 独立重建归档判定并核验不可变文件哈希。

## 科学结果

三个预设展示条件的配对 ΔR 为 0.07337–0.07568。移除调制后仍有 29.5 Hz 的基线振荡。21 项步长收敛检查通过，最大绝对 ΔR 为 0.00003165。每条敏感性轨道有 18/49 个网格点满足完整判据，14/49 个点的配对基线不合格。结果支持锁定的示意性模型中的输入干预效应。三个轨道是初始状态和观测种子的敏感性检查。EEG 代理是合成观测，扫描结论限于已采样点。详见[结果评估](theta_gamma/evidence/result-assessment.md)与[独立评审](theta_gamma/reviews/iteration-1.md)。

## API 与执行路径

- `model.py` 通过 `WilsonCowanStep` 建立 E/I 动力学，用 `braintools.init.Constant` 初始化，BrainUnit 表达步长、时间与输入频率。时间输入回调表达指定的 theta 调制。BrainMass `Simulator.run` 管理 State 初始化、编译时间循环、采样和监测，49 个条件走原生模型轴，3 条敏感性轨道走原生 batch 轴。归档耗时包含编译与执行。
- `analysis.py` 使用 BrainTools 的带通、解析信号和 Welch PSD，保留单位感知的采样间隔。预先指定的外部相位与逐周期旋转由宿主统计处理，单信号 PAC 接口会自行提取相位，无法直接表达这一对照。合成观测、配对噪声、判据、验证与序列化由实验代码处理。[BrainTools API](https://brainx.chaobrain.com/braintools/apis/analysis.html) · [接口缺口记录](theta_gamma/evidence/api-gap.md)
- `plot_results.py` 使用 `brainmass.viz.plot_timeseries` 绘制 E/I 轨迹，并用 Matplotlib 组合相位剖面、频谱和非等距扫描网格。实验启动、产物清单和报告属于宿主编排。[BrainMass 文档](https://brainx.chaobrain.com/brainmass/)

## 版本相关的接口冲突

公开 Wilson–Cowan API 叙述把 `wEI` 标作 I→E，仓库 BrainMass 模型参考沿用该定义。本次镜像的 BrainMass 0.1.1 在该实验的非对称测试状态下表现相反。仅在临时副本中把生产代码的 `wIE=12g, wEI=15g` 换成按文档方向填写的 `wEI=12g, wIE=15g`，测试在第一项解析导数检查失败。观察值为 (0.01939118324, −0.00547613392) /ms，锁定方程要求 (0.03233539001, −0.00284852925) /ms。归档版本的映射通过同一测试，并由单步测试交叉核对。该证据限定于所测镜像和版本。[公开 API](https://brainx.chaobrain.com/brainmass/reference/generated/brainmass.WilsonCowanStep.html) · [归档差异记录](theta_gamma/evidence/api-direction-discrepancy.md)

这条运行是更换镜像后的描述性基线。按仓库精炼流程，将方向冲突保留为本次诊断证据。未来跨版本复用时，以非对称权重和解析导数对照验证关键字方向。

## 迁移补查

在同一新镜像中，只读载入正式运行的 `raw/trajectories.npz` 和 `metrics/analysis.npz`。保持新版的固定展示点和观测定义，补做旧实验的两项检查。结果属于事后迁移复核，原规格和评审记录照常适用。

- **自主载波。** 对相对增益 1、无调制条件的三个敏感性设置，在 3–13 s 分别检查 E 和 I。用峰突出度 0.2、最短峰距 4 ms、至少 20 个峰、峰峰值大于 0.05、周期 CV 小于 0.2，以及周期计数与 1–120 Hz 主谱峰相差不超过 2 Hz 的旧阈值。每组 E/I 均检测到 292 个峰，周期计数频率为 29.264–29.267 Hz，Welch 主峰为 29.5 Hz，周期 CV 为 0.01095–0.01104。三组均通过 E/I 一致性检查。
- **时间子窗。** 对保存的合成 EEG 代理 gamma 包络与已知外部 theta 相位重算配对 R。5–10 s 的三组 ΔR 为 0.07098、0.07326、0.07231。10–11.5 s 的三组 ΔR 为 0.07081、0.07174、0.07076。两窗的六组比较均为正且超过 0.05。此处仅复核方向与效应大小，沿用正式运行已保存的全窗替代检验。
