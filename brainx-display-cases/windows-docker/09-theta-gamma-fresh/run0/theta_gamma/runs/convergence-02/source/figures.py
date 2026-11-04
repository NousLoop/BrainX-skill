"""Evidence-bound static figures. Diagnostic until independent review passes."""
import argparse
import json
from pathlib import Path

import brainmass
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def save(fig, path):
    fig.tight_layout()
    fig.savefig(path.with_suffix(".png"),dpi=200,bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"),bbox_inches="tight")
    plt.close(fig)


def main():
    p=argparse.ArgumentParser(); p.add_argument("--mode",choices=["diagnostic","final"],default="diagnostic")
    p.add_argument("--run",default="runs/production-02"); a=p.parse_args()
    run=Path(a.run); out=Path("figures")/(a.mode+"-iteration-2"); out.mkdir(parents=True,exist_ok=True)
    if a.mode=="final":
        acceptance=json.loads(Path("reviews/acceptance.json").read_text())
        assert acceptance["verdict"]=="PASS"
    raw=np.load(run/"raw/trajectories.npz"); d=np.load(run/"raw/derived.npz")
    rows=json.loads((run/"metrics/metrics.json").read_text())
    g=raw["gains_flat"]; m=raw["depths_flat"]
    pair=[int(np.flatnonzero((g==1)&(m==v))[0]) for v in [0,.75]]
    t=raw["t_s"]; select=(t>=3)&(t<3.5)
    colors=["#0072B2","#D55E00"]
    fig,ax=plt.subplots(3,2,figsize=(12,8),sharex=True,sharey="row")
    for col,c in enumerate(pair):
        brainmass.viz.plot_timeseries(np.column_stack([raw["E"][select,0,c],raw["I"][select,0,c]]),
            ts=t[select],labels=["E","I"],ax=ax[0,col])
        ax[0,col].set_title(f"m={m[c]:.2f}, g=1 | {a.mode}")
        ax[0,col].set(ylim=(0,1),ylabel="population activity")
        ax[0,col].set_xlabel("time (s)")
        ax[1,col].plot(t[select],d["proxy"][select,0,c],color=colors[col],label="EEG proxy")
        ax[1,col].plot(t[select],d["base_proxy"][select,0,c],color="black",ls=":",label="without theta mixture")
        ax[1,col].set(ylim=(-.5,1.2),ylabel="proxy (a.u.)")
        ax[1,col].legend(fontsize=8)
        ax[2,col].plot(t[select],d["gamma_envelope"][select,0,c],color=colors[col],label="25–100 Hz envelope")
        ax[2,col].plot(t[select],.2+.15*np.cos(d["phase_rad"][select]),color="0.5",ls="--",label="theta phase reference (scaled)")
        ax[2,col].set(xlim=(3,3.5),ylim=(0,.6),xlabel="time (s)",ylabel="envelope (a.u.)")
        ax[2,col].legend(fontsize=8)
    save(fig,out/"traces")

    fig,ax=plt.subplots(1,3,figsize=(15,4))
    for col,c in enumerate(pair):
        label=f"m={m[c]:.2f}"
        ax[0].semilogy(d["freqs_hz"],d["psd"][0,:,0,c],color=colors[col],ls=["--","-"][col],label=label)
        ax[1].plot(d["phase_bin_centers_rad"],d["phase_curves"][0,0,c],marker=["o","s"][col],
                   color=colors[col],ls=["--","-"][col],label=label)
        null=d["surrogates_R"][0,0,c]
        row=next(r for r in rows if r["view"]=="proxy" and r["rep"]==0 and r["condition"]==c)
        ax[2].hist(null,bins=np.linspace(0,1,31),alpha=.45,color=colors[col],label=label+" cycle null")
        ax[2].axvline(row["surrogate_observed_R"],color=colors[col],ls=["--","-"][col],label=label+" observed")
    ax[0].set(xlim=(0,120),ylim=(1e-12,1),xlabel="frequency (Hz)",ylabel="PSD (a.u.²/Hz)",title="EEG proxy power spectrum")
    ax[1].set(xlim=(-np.pi,np.pi),ylim=(0,.6),xlabel="known theta phase (rad; 0=drive max)",ylabel="mean gamma envelope (a.u.)",title="Phase nesting, fixed g=1")
    ax[2].set(xlim=(0,1),xlabel="R on complete theta cycles",ylabel="surrogate count",title="199 phase rotations per cycle")
    for axis in ax: axis.legend(fontsize=8)
    fig.suptitle(a.mode+" | first initial condition; deterministic example")
    save(fig,out/"nesting")

    grid=[]
    for key in ["R","gamma_fraction","defined_peak_hz"]:
        values=np.array([[r[key] if r[key] is not None else np.nan for r in rows
                         if r["view"]=="no_theta" and r["rep"]==rep] for rep in range(3)])
        # Mean of ICs only when all are defined. No uncertainty inference.
        grid.append(values.mean(axis=0).reshape(5,5))
    delta=grid[0]-grid[0][0:1,:]
    fig,ax=plt.subplots(1,4,figsize=(16,4))
    for axis,values,title,lo,hi,cmap in zip(ax,[grid[0],delta,grid[1],grid[2]],
        ["R (without theta mixture)","ΔR relative to m=0","gamma fraction (1–120 Hz)","valid gamma band peak (Hz)"],
        [0,-1,0,25],[1,1,1,100],["viridis","coolwarm","viridis","viridis"]):
        im=axis.imshow(values,origin="lower",aspect="auto",interpolation="none",vmin=lo,vmax=hi,cmap=cmap)
        axis.set_xticks(range(5),d["gain_axis"]); axis.set_yticks(range(5),d["depth_axis"])
        axis.set(xlabel="E↔I loop gain g",ylabel="modulation depth m",title=title)
        fig.colorbar(im,ax=axis,shrink=.8)
        for row in range(5):
            for col in range(5):
                valid=all(r["valid_gamma"] for r in rows if r["view"]=="no_theta" and r["condition"]==row*5+col)
                baseline=all(r["autonomous_gamma_predicate"] for r in rows if r["view"]=="no_theta" and r["depth"]==0 and r["gain"]==d["gain_axis"][col])
                if not valid: axis.text(col,row,"×",ha="center",va="center",color="red",fontsize=13)
                elif not baseline: axis.text(col,row,"○",ha="center",va="center",color="red",fontsize=13)
    fig.suptitle(a.mode+" | 3-IC mean; × invalid band/timing; ○ no autonomous gamma at matched m=0")
    save(fig,out/"scan")
    (out/"source.json").write_text(json.dumps({"run":str(run),"manifest":str(run/"manifest.json"),
        "mode":a.mode,"pair_conditions":pair,"IC":0,"scan_reduction":"mean of 3 ICs, no CIs",
        "source":"figures.py","outputs":["traces","nesting","scan"]},indent=2))


if __name__=="__main__": main()
