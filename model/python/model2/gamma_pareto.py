# -*- coding: utf-8 -*-
"""
Gamma grid evaluation and Pareto filtering for robust solutions
"""
from typing import Dict, Tuple, Iterable, List, Optional, Any


def evaluate_gamma(gamma: float, builder):
    """Build and solve model for a given gamma, return (gamma, metrics)."""
    model, x = builder(gamma)
    model.solve()
    metrics = {
        "r_min":     model.attr("r_min"),
        "r_nom":     model.attr("r_nom"),
        "r_avg":     model.attr("r_avg"),
        "viol_rate": model.attr("viol_rate"),
        "switches":  model.attr("switches"),
        "peak_res":  model.attr("peak_res"),
    }
    return gamma, metrics


def pareto_filter(candidates: Iterable[Tuple[float, Dict[str, float]]]):
    """Return non-dominated (gamma, metrics) under specified criteria."""
    cand = list(candidates)
    front: List[Tuple[float, Dict[str, float]]] = []
    for g, m in cand:
        dominated = False
        for _, n in cand:
            if n is m:
                continue
            if (
                n["r_min"] >= m["r_min"]
                and n["switches"] <= m["switches"]
                and n["peak_res"] <= m["peak_res"]
                and n["r_nom"] >= m["r_nom"]
            ):
                dominated = True
                break
        if not dominated:
            front.append((g, m))
    return front


def gamma_grid_search(
    gammas: Iterable[float],
    X: float,
    Ypct: float,
    builder,
) -> Optional[float]:
    """Evaluate grid, screen by thresholds, Pareto filter, and select."""
    evaluated = [evaluate_gamma(g, builder) for g in gammas]
    screened = [
        (g, m) for g, m in evaluated
        if (m["r_min"] >= X and m["viol_rate"] <= Ypct / 100.0)
    ]
    front = pareto_filter(screened)
    front.sort(key=lambda gm: (-gm[1]["r_min"], gm[1]["switches"], gm[1]["peak_res"]))
    return front[0][0] if front else None
