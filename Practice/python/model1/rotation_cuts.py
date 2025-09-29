# -*- coding: utf-8 -*-
"""
Rotation window cuts (minimum spacing) with violation scanning.

This module provides a minimal, auditable implementation for enforcing
crop rotation windows of length L_k across a cyclic season order. The
core idea is to avoid generating all window constraints upfront (which
can be exponential in count when enumerated naïvely). Instead, we scan
the current solution for violations and add only the needed window
inequalities on demand.

Inputs (conceptual)
-------------------
Lk: Dict[crop, int]
    Minimum spacing window length per crop k.
seasons: Dict[str, Any]
    Contains a season order list under key 'order' and a shift function
    under key 'shift' that maps (season, delta) -> shifted season.
model: Any
    An abstract MIP model interface exposing add_constr().
z: Dict[Index, Any]
    Decision variables indexed by (t, s, i, k), compatible with model.
"""
"""
Outputs
-------
int
    Number of added window inequalities (for auditing and convergence
    tracking).

Notes on complexity & reproducibility
-------------------------------------
- Precomputing windows is O(|K| * L_k * |S|) and scanning is near-linear
  in the number of windows. Index compression and vectorized summations
  can substantially reduce constant factors.
- For stable experiments, fix random seeds and keep a consistent index
  order; log per-iteration counts of newly added constraints.
"""
from typing import Dict, Tuple, List, Any

Index = Tuple[int, Any, Any, Any]  # (t, s, i, k)


def generate_windows(Lk: Dict[Any, int], seasons: Dict[str, Any]) -> Dict[Any, List[List[Any]]]:
    """Generate sliding windows for each crop k of length L_k across seasons order."""
    windows: Dict[Any, List[List[Any]]] = {}
    for k, L in Lk.items():
        wins: List[List[Any]] = []
        for s in seasons['order']:
            win = [seasons['shift'](s, d) for d in range(L)]
            wins.append(win)
        windows[k] = wins
    return windows


def scan_and_add_rotation_cuts(
    model: Any,
    z: Dict[Index, Any],
    Lk: Dict[Any, int],
    seasons: Dict[str, Any],
) -> int:
    """Add sum_{d=0}^{L_k-1} z_{t,s+d,i,k} <= 1 whenever violated."""
    windows = generate_windows(Lk, seasons)
    added = 0
    tik = {(t, i, k) for (t, s, i, k) in z.keys()}
    for (t, i, k) in tik:
        for win in windows[k]:
            keys = [(t, s, i, k) for s in win]
            total = sum(int(z.get(key, 0)) for key in keys)
            if total > 1:
                model.add_constr(sum(z[key] for key in keys) <= 1)
                added += 1
    return added
