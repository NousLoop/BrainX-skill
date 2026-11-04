# Theta–gamma BrainX demonstration

中文结果、模型边界和图：[report.md](report.md)。

- 当前锁定规格：[NeuroSpecification.md](NeuroSpecification.md)。
- 当前原始数据与完整溯源：[production-02 manifest](runs/production-02/manifest.json)。
- 数值复算：[convergence-02 manifest](runs/convergence-02/manifest.json)。
- 初版失败与保留结果：[iterations/iteration-1/report.md](iterations/iteration-1/report.md)。
- 独立 review：[reviews](reviews/)；未 PASS 前图均为 diagnostic。

使用现有 `/brainx-venv/bin/python`，从本目录运行：

```bash
JAX_PLATFORMS=cpu JAX_ENABLE_X64=true python verify.py
python launch.py smoke smoke-replication
python launch.py production production-replication
python launch.py convergence convergence-replication
```

每个 run 名必须是新名字；launch 会冻结配置、源代码、环境、命令和 SHA256，
并保留日志、退出码、原始 NPZ 和指标。不会安装或更改依赖。
报告和绘图脚本默认读取已完成的 `*-02` 运行；复算运行的指标位于其自身目录。

模型仅作 illustrative / phenomenological 演示；没有实测 EEG 或生物机制唯一性主张。
