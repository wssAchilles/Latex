# -*- coding: utf-8 -*-
"""
Bertsimas–Sim (BS) budget uncertainty robust counterpart builder
"""
from typing import Dict, Any


def robustify_constraint(
    model: Any,
    a0: Dict[Any, float],
    d: Dict[Any, float],
    x: Dict[Any, Any],
    b: float,
    Gamma: float,
    name: str = "rc",
):
    """Build BS robust counterpart: a0·x + sum_j d_j s_j + Gamma*theta <= b, 0<=s_j<=theta."""
    theta = model.add_var(name=f"{name}_theta", lb=0)
    s = {j: model.add_var(name=f"{name}_s_{j}", lb=0) for j in d}
    lhs = sum(a0.get(j, 0.0) * x[j] for j in x) \
          + sum(d[j] * s[j] for j in d) \
          + Gamma * theta
    model.add_constr(lhs <= b, name=f"{name}_main")
    for j in d:
        model.add_constr(s[j] <= theta, name=f"{name}_ub_{j}")
    return theta, s
