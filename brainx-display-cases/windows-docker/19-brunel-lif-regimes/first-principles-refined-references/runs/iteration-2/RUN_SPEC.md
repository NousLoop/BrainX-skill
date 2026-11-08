# Immutable iteration-2 analysis contract

No new simulation. Parent baseline-v1 raw spikes/graphs are referenced via symlinks, with parent manifest and every raw hash verified. Original production and its manifest remain intact. Scientific configuration/specification/seeds/time windows/decision thresholds are unchanged.

Use documented BrainTools spectrogram, dt=0.1 ms, Hann/10000 samples/5000 overlap/constant segment detrend; average the segment axis. Full-window boxcar/zero-overlap/constant detrend gives the periodogram. Quantities preserve Hz input and Hz²/Hz PSD; scoped float64 analysis matches the original float64 host analysis, independently of the float32 dynamics.

Compare all frequencies and PSDs against original saved arrays (rtol=1e-9, atol=1e-11), all scalar metrics (rtol=1e-9, atol=1e-10), every categorical predicate and every final condition decision. Preserve differences and reject changed decisions. Save new metrics, assessment, parity, timing, code/environment/config identity, logs and hashes. No model optimization or new scientific execution is justified by this analysis-only correction.
