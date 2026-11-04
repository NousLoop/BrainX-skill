# NeuroSpecification

- Status: locked
- Clarification gate: complete
- Researcher approval: 用户明确授权直接选择并锁定全部其余科学与数值设置；无需再次询问或等待确认（2026-11-03）。

## Researcher request
- Brain-modeling question or behavior: 构建 theta 调制的 E-I gamma 群体回路，展示相位嵌套；移除调制，比较嵌套和模拟 EEG 代理；扫描调制深度及 gamma 回路增益。
- Requested model, experiment, or comparison: 单个 Wilson–Cowan E/I 群体回路，外加规定的 6 Hz 正弦驱动；成对移除该驱动的周期项。仅为 illustrative / phenomenological 模型。
- Execution mode: forward-simulation
- Required outputs: 原始 E/I 与输入时序、模拟 EEG 代理、功率谱、gamma 包络与 theta 相位关系、相位振幅耦合指标、二维扫描、数值和观测映射敏感性、完整失败记录、独立 Codex MCP review、中文报告。
- Constraints: 不声称生物真实性、实测 EEG 拟合或机制唯一性；保留不支持预期的设置。使用现有 BrainX 环境；无训练、无拟合。计算预算不足即保存状态并停止。
- Open decisions and handling: 所有剩余选择由用户委托，以下为代理选择；无待答问题。选择 CPU 与确定性模型，不新增依赖。实现与试验配置在查看生产结果前冻结。

## Inspected data contract
- Data sources and inspected contents: /workspace 初始为空；无实验数据。所有结果均为模拟。
- Shapes, axes, sampling/time base, and physical units: time × condition × initial-condition replicate；E/I 为无量纲归一化活动；时间 ms，频率 Hz，EEG 代理为 arbitrary units。
- Required preprocessing and the subset used to fit each transform: 丢弃前 2 s；生产总长 12 s，dt=0.1 ms，分析降采样至 1 kHz；滤波边缘再各去 0.5 s。预先固定 theta=4–8 Hz、gamma=25–100 Hz；无数据拟合的预处理。
- Mapping from data to model inputs, targets, and observables: τE dE/dt=−E+S_E(16E−12g I+P(t)); τI dI/dt=−I+S_I(15g E−3I+Q)。S_E(x)=logistic[1.3(x−4)]，S_I(x)=logistic[2(x−3.7)]；τE=2.5 ms，τI=5 ms，Q=0，P(t)=1.25+m cos(2π6t)。初值 (E,I)=(0.1,0.1),(0.11,0.09),(0.09,0.11)。gain g 同时缩放两个 E↔I 交叉连接，保留各自符号。
- Known data limitations or unresolved mismatches: EEG proxy y=E−0.5I+0.2 cos(theta phase)，相位使用已知外部驱动，另记录从代理估计相位的可靠性。敏感性观测 y=E、E−I 及无 theta 混入版本；该线性代理没有体积传导、参考电极或仪器模型。
- Conditional interpretations of unanswered experimental questions: 没有实测条件；所有解释均为该规定输入和模型下的条件性结论。

## Acceptance boundary
- Evidence required for success, failure, or an inconclusive result: 预定展示 m=0 与 m=0.75,g=1；完整扫描 m=[0,0.25,0.5,0.75,1],g=[0.8,0.9,1,1.1,1.2]，每点 3 初值。若未出现 gamma 或无清晰嵌套，报告失败/部分支持，不移动展示点。gamma 有效性要求 25–100 Hz 峰、带内相对功率>0.1 且包络均值>1e−4。嵌套以已知 theta 相位与 gamma 包络的一阶向量强度 R、18-bin Tort MI 及相位曲线衡量；强支持要求有效 gamma、R 调制−无调制>0.05、调制点超过逐周期随机相位 surrogate 的 95% 分位。周期 surrogate 199 次，seed=20261103；不把重复初值视为独立动物样本或 population inference。
- Required baselines and controls: 每个 g、每个初值均有 m=0；同一路径原生批处理；相同输入均值、初值、求解器与时间窗。保留 m=0 的外部 6 Hz 相位标签和相同 EEG theta 项，以区分动力学调制与线性观测混合。另保存无 theta 混入的代理、E 与 I 本身。固定 g=1 展示点做 dt=0.05 ms 复算，并在 5–10 s 与 10–11.5 s 子窗检查方向；生产结果不能用于调参。
- Invalid-result conditions: 非有限/越界状态、控制输入不匹配、不可复现、未完成原始数据、数值复算 R 差>0.02 或峰频差>2 Hz（未解释）均阻止强结论。无 gamma 的点标为无有效 gamma，仍保存原始连续指标；不能仅从 PAC 数值宣布 gamma 嵌套。
- Allowed claims and explicit non-claims: 可以展示在指定参数下 theta 输入对 E/I gamma 包络与代理信号的条件性影响；不得把代理当作 EEG、将 PAC 当成独特机制识别、将初值差异当成统计独立性、或宣称扫描得到连续区域边界。多重扫描结果为描述性。
- Model/comparison rationale and decisive assumption checks: 因果链为 theta 周期输入→E/I 动力学→gamma 包络→线性代理。m=0 控制隔离周期输入；多种观测映射与无 theta 混入对照检验观测伪影。外源 theta 不代表内源 theta 生成；本项目不比较未建模的生物机制。文献门跳过：经授权的现象学标准 WC 回路，没有待验证的生物真实性主张。
