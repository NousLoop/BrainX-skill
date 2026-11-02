"""Render the unaccepted iteration-1 diagnostic figure."""

from __future__ import annotations

import json
from pathlib import Path

import brainmass
import brainunit as u
import matplotlib.pyplot as plt
import numpy as np


RUN = Path("/workspace/runs/alpha-production-20261102-i1")
OUTPUT = Path("/workspace/figures/iteration-1-diagnostic.png")
COLORS = ("#0072B2", "#E69F00", "#009E73", "#CC79A7")
LABELS = ("100%", "75%", "50%", "25%")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with np.load(RUN / "results.npz") as data:
        times_s = data["times_s"]
        eeg_mv = data["eeg_mv"]
        frequencies_hz = data["frequencies_hz"]
        power = data["power_mv2_per_hz"]
        rms_mv = data["rms_mv"]
        retention = data["retention_fractions"]
    convergence = json.loads((RUN / "convergence.json").read_text())["checks"]

    retained = times_s >= 4.0
    trace_values = eeg_mv[retained, :, 0]
    trace_values = trace_values - np.mean(trace_values, axis=0, keepdims=True)
    traces = trace_values * u.mV
    trace_times = times_s[retained] * u.second

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.0))
    brainmass.viz.plot_timeseries(
        traces,
        ts=trace_times,
        labels=list(LABELS),
        ax=axes[0, 0],
    )
    axes[0, 0].set(
        title="A  Cortical EEG proxy, first initial state",
        xlabel="time (s)",
        ylabel="demeaned proxy (mV)",
        ylim=(-3.5, 3.5),
    )

    spectral_band = (frequencies_hz >= 4.0) & (frequencies_hz <= 30.0)
    for index, (label, color) in enumerate(zip(LABELS, COLORS, strict=True)):
        axes[0, 1].semilogy(
            frequencies_hz[spectral_band],
            power[spectral_band, index, 0],
            label=label,
            color=color,
            linewidth=1.8,
        )
    axes[0, 1].axvspan(8.0, 13.0, color="0.85", zorder=0, label="alpha band")
    axes[0, 1].set(
        title="B  Locked Welch spectra, same state",
        xlabel="frequency (Hz)",
        ylabel="PSD (mV²/Hz)",
        xlim=(4.0, 30.0),
    )
    axes[0, 1].legend(frameon=False, ncol=2, fontsize=8)

    x = np.arange(retention.size)
    for initial_index in range(rms_mv.shape[1]):
        axes[1, 0].plot(
            x,
            rms_mv[:, initial_index],
            color="0.72",
            linewidth=0.8,
            marker="o",
            markersize=2.5,
        )
    axes[1, 0].plot(
        x,
        np.median(rms_mv, axis=1),
        color="black",
        linewidth=2.0,
        marker="o",
        label="median",
    )
    axes[1, 0].axhline(0.01, color="#D55E00", linestyle="--", label="peak-valid RMS floor")
    axes[1, 0].set_yscale("log")
    axes[1, 0].set(
        title="C  Paired retained RMS (n=8 initial states)",
        xlabel="retained inhibitory gain",
        ylabel="RMS (mV, log scale)",
        xticks=x,
        xticklabels=LABELS,
    )
    axes[1, 0].legend(frameon=False, fontsize=8)

    convergence_x = np.arange(len(convergence))
    convergence_percent = [100.0 * item["rms_relative_difference"] for item in convergence]
    axes[1, 1].bar(
        convergence_x,
        convergence_percent,
        color=(COLORS[0], COLORS[3]),
        width=0.65,
    )
    axes[1, 1].axhline(5.0, color="#D55E00", linestyle="--", label="locked 5% limit")
    axes[1, 1].set(
        title="D  Half-step RMS convergence fails",
        xlabel="retained inhibitory gain",
        ylabel="relative RMS difference (%)",
        xticks=convergence_x,
        xticklabels=("100%", "25%"),
    )
    axes[1, 1].legend(frameon=False, fontsize=8)

    fig.suptitle("Diagnostic, unaccepted iteration 1 — numerical validity failed", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUTPUT, dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
