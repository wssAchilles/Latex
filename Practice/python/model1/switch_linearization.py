# -*- coding: utf-8 -*-
"""
Switch cost adjacency linearization with incremental cut generation
"""
from typing import Dict, Tuple, Iterable, List, Any

Index = Tuple[int, Any, Any, Any]  # (t, s, i, k)
Switch = Tuple[int, Any, Any, Any, Any]  # (t, s, i, k, k')


def detect_switch_violations(
    z: Dict[Index, int],
    seasons: Dict[str, Any],
    neighbors: Iterable[Tuple[Any, Any]],
) -> List[Switch]:
    """Scan adjacent seasons and collect switch occurrences that need w-vars."""
    violations: List[Switch] = []
    tis = {(t, i) for (t, s, i, k) in z.keys()}
    for (t, i) in tis:
        for s in seasons['order']:
            s_next = seasons[(s, 'next')]
            for (k, kp) in neighbors:
                if z.get((t, s, i, k), 0) == 1 and z.get((t, s_next, i, kp), 0) == 1:
                    violations.append((t, s, i, k, kp))
    return violations


def add_switch_cuts(
    model: Any,
    z: Dict[Index, Any],
    seasons: Dict[str, Any],
    w: Dict[Switch, Any],
    kappa: Dict[Tuple[Any, Any], float],
    violations: Iterable[Switch],
) -> None:
    """Add adjacency linearization constraints and objective terms for switches."""
    for (t, s, i, k, kp) in violations:
        key = (t, s, i, k, kp)
        if key not in w:
            w[key] = model.add_var(name=f"w_{t}_{s}_{i}_{k}_to_{kp}", lb=0, ub=1, vtype='B')
            model.add_constr(w[key] >= z[(t, s, i, k)] + z[(t, seasons[(s, 'next')], i, kp)] - 1)
            model.add_constr(w[key] <= z[(t, s, i, k)])
            model.add_constr(w[key] <= z[(t, seasons[(s, 'next')], i, kp)])
            model.add_obj_term(kappa[(k, kp)] * w[key])


def incremental_switch_linearization(
    model: Any,
    z: Dict[Index, Any],
    seasons: Dict[str, Any],
    neighbors: Iterable[Tuple[Any, Any]],
    kappa: Dict[Tuple[Any, Any], float],
    max_iter: int = 10,
) -> Dict[Switch, Any]:
    """Iteratively solve, detect violations, and add missing adjacency cuts."""
    w: Dict[Switch, Any] = {}
    for _ in range(max_iter):
        model.solve()
        vio = detect_switch_violations(z, seasons, neighbors)
        if not vio:
            break
        add_switch_cuts(model, z, seasons, w, kappa, vio)
    return w
