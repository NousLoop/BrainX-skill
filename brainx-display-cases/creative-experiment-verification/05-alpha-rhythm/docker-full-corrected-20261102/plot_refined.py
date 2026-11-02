"""Render saved, unit-declared evidence without recomputing its Welch spectra."""
import argparse
import json
from pathlib import Path
import re

import brainmass
import brainunit as u
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--run-dir", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--mode", choices=["diagnostic", "final"], required=True)
parser.add_argument("--review-file", type=Path)
args = parser.parse_args()
if args.mode == "final":
    if not args.review_file or not re.search(r"\*\*OUTCOME:\*\*\s*`?PASS", args.review_file.read_text()):
        raise RuntimeError("Final figures require a saved independent PASS review")
config = json.loads((args.run_dir / "config.json").read_text())
convergence = json.loads((args.run_dir / "convergence.json").read_text())["checks"]
with np.load(args.run_dir / "results.npz") as saved:
    time = saved["times_s"]
    raw = saved["eeg_mv"]
    record = round(1 / config["dt_ms"])
    first = round(2000 / config["dt_ms"]) + record - 1
    ts = time[first::record]
    traces = raw[first::record, :, 0]
    traces = traces - traces.mean(axis=0, keepdims=True)
    frequency = saved["frequencies_hz"]
    power = saved["power_mv2_per_hz"][:, :, 0]
    rms = saved["rms_mv"]
    retention = saved["retention_fractions"]
labels = [f"{100 * value:g}% inhibition gain" for value in retention]
colors = ["#0072B2", "#D55E00", "#009E73", "#CC79A7"]
styles = ["-", "--", "-.", ":"]
fig, axes = plt.subplots(2, 2, figsize=(11, 7.5))
display = ts >= 4.0
brainmass.viz.plot_timeseries(traces[display] * u.mV, ts=ts[display] * u.second,
                            labels=labels, ax=axes[0, 0])
for line, color, style in zip(axes[0, 0].lines, colors, styles):
    line.set_color(color)
    line.set_linestyle(style)
axes[0, 0].set(title="A  EEG proxy: first paired initial state", xlabel="Time (s)",
               ylabel="Demeaned cortical proxy (mV)", xlim=(4, 6), ylim=(-3.5, 3.5))
axes[0, 0].legend(fontsize=8, loc="lower left")
show = (frequency >= 4) & (frequency <= 30)
for index in range(4):
    axes[0, 1].semilogy(frequency[show], power[show, index], color=colors[index],
                       linestyle=styles[index], label=labels[index])
axes[0, 1].axvspan(8, 13, color="gray", alpha=0.12)
axes[0, 1].set(title="B  Saved Welch PSD (quiet peaks undefined)", xlabel="Frequency (Hz)",
               ylabel="Power spectral density (mV²/Hz)", xlim=(4, 30))
for index in range(4):
    x = index + np.linspace(-0.08, 0.08, 8)
    axes[1, 0].scatter(x, rms[index], s=22, color=colors[index], alpha=0.8)
    axes[1, 0].plot([index-0.12, index+0.12], [np.median(rms[index])]*2, color="black")
axes[1, 0].axhline(0.01, color="black", linestyle=":", linewidth=1, label="Oscillation floor")
axes[1, 0].set(title="C  All 8 paired initial states; black = median", ylabel="Retained RMS (mV)",
               xticks=range(4), xticklabels=[f"{100*x:g}%" for x in retention], xlabel="Retained inhibition gain")
axes[1, 0].legend(fontsize=8)
ratios = []
for condition in range(4):
    checks = [c for c in convergence if c["condition_index"] == condition]
    values = [c["rms_absolute_difference_mv"] / max(0.05 * abs(c["half_step_rms_mv"]), 1e-6)
              for c in checks]
    ratios.extend(values)
    axes[1, 1].scatter(condition + np.linspace(-0.08, 0.08, len(values)), values,
                       s=22, color=colors[condition], alpha=0.8)
axes[1, 1].axhline(1, color="black", linestyle="--", label="Acceptance bound")
axes[1, 1].set(title="D  Full-grid half-step RMS check", ylabel="RMS error / allowed tolerance",
               xticks=range(4), xticklabels=[f"{100*x:g}%" for x in retention],
               xlabel="Retained inhibition gain", ylim=(0, max(1.15, 1.1*max(ratios))))
axes[1, 1].legend(fontsize=8)
title = "Inhibitory-gain reduction in a Jansen–Rit cortical column"
if args.mode == "diagnostic":
    title = "DIAGNOSTIC — not yet independently accepted\n" + title
fig.suptitle(title, fontsize=13)
fig.tight_layout()
args.output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output, dpi=300, bbox_inches="tight")
fig.savefig(args.output.with_suffix(".pdf"), bbox_inches="tight")
plt.close(fig)
print(args.output)
