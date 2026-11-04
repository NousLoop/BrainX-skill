# Preserved failures and unfavorable evidence

## Implementation construction failure (iteration 1)
`checks/first-construction.log`: attempted monitor read of environment t raised
KeyError. Simulator evaluates monitors outside the input time scope. No result
was produced. Corrected by recording the actually applied E input in a registered
ShortTermState inside update; inherited update and integration remain unchanged.
No scientific setting changed and no production outcome had been inspected.

## Documentation and API failures
See brainx-study-record.md for absent optional BeautifulSoup and two documentation
404s; standard HTMLParser and official index resolved them without installation.
`docs/api_execution_checks.json` preserves missing analysis namespace errors.

## Scientific null / unfavorable results
Iteration 1 production retained in full. The fixed-pair gamma-band nesting predicate
passes, but a post-run fundamental audit finds ~22 Hz E cycles, with a 43.5 Hz harmonic.
This fails to establish the requested autonomous gamma circuit. The scientific
outcome is partially_supported. No current production parameter has been changed.
The entire initial scan (including all invalid-gamma points) remains available.

## Independent-solver transient check failure
`checks/verification-failed-1.log` and `checks/solver-diagnostic.log`: a heuristic
absolute 0.03 cutoff at dt=0.1 ms failed (max error 0.03441 over the first 20 ms).
Halving dt reduced error to 0.01722 and quartering to 0.00861. This is expected
first-order Euler trajectory/phase error. The focused witness now requires
first-order convergence at all three spacings and <0.01 error at 0.025 ms.
This verification change is disclosed; no model parameter or production setting
was altered. The locked production acceptance still requires R difference ≤0.02
and spectral peak difference ≤2 Hz under dt halving; failure there blocks strong claims.

## Synthetic metric witness design failure
`checks/verification-failed-2.log` and `checks/metric-diagnostic.log`: comparing
known-reference AM MI to native single-signal MI failed when the synthetic signal
contained only a modulated 60 Hz carrier, with no 6 Hz component from which to
estimate phase (MI 0.01025 versus known-reference 0.03238). Adding the declared
0.2 theta component to that witness yields native MI 0.03239. The corrected parity
witness compares compatible observations; the original failure remains evidence
that single-signal phase extraction can be ill-defined. Primary R stayed 0.29996
versus analytic 0.3, and linear-mixture null R was 0.00000244.
