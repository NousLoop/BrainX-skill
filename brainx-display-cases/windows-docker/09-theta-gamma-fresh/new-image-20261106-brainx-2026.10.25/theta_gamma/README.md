# Theta-modulated E–I gamma mass circuit

中文结果与三组配对图见 [report.md](report.md)。范围严格为 illustrative / phenomenological：合成 EEG 代理、外部指定 theta、无实验数据或机制唯一性推断。

- 规格：[NeuroSpecification.md](NeuroSpecification.md)
- 模型与分析：[model.py](model.py)、[analysis.py](analysis.py)
- 冻结运行与实验：[launch.py](launch.py)、[experiment.py](experiment.py)
- 验证与独立重建：[test_checks.py](test_checks.py)、[assess_results.py](assess_results.py)
- 正式证据：`runs/production-02/`；旧版与失败记录仍在 `runs/`、`evidence/`。
- 每点结果：[evidence/sweep.csv](evidence/sweep.csv)
- 图源与证据清单：[plot_results.py](plot_results.py)、[FIGURE_MANIFEST.md](FIGURE_MANIFEST.md)
- 独立审查：`reviews/`，最终结论以 report 中的审查状态为准。

当前 Python：`/brainx-venv/bin/python`，CPU、float64。环境与全部分发版本在 `runs/production-02/environment.json`；本项目未修改安装环境。

```bash
cd /workspace/theta_gamma
JAX_PLATFORMS=cpu /brainx-venv/bin/python test_checks.py
JAX_PLATFORMS=cpu /brainx-venv/bin/python launch.py production-replay production_exact_config.json
JAX_PLATFORMS=cpu /brainx-venv/bin/python plot_results.py --run production-replay --mode diagnostic
```

新运行必须使用新 ID。`final` 绘图只允许与 `reviews/gate.json` 中 PASS 对应的 run ID；新运行先画 diagnostic，不能套用旧运行审查。`assess_results.py` 则专门复核保存的正式 production-02 证据。

数据轴和字段见 [evidence/data-dictionary.md](evidence/data-dictionary.md)。原始运行快照不覆盖；代码、配置、环境、种子、时间和来源哈希均保存。
