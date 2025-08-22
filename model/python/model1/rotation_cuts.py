# -*- coding: utf-8 -*-
"""
Rotation (minimum spacing) window cuts with violation scanning
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
