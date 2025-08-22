"""
Rolling optimization with CVaR (didactic demo).

This minimal example shows a one-dimensional annual decision (total supply q)
under price-supply feedback with capacity cap C. We evaluate decisions via
expected profit minus lambda * CVaR_alpha(loss), using an empirical CVaR.

It is intended for explanatory listings, not production use.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Iterable
import numpy as np


# --- Basic economics: linear price and capacity-capped sales ---
def linear_price(q: np.ndarray, a: float, b: float) -> np.ndarray:
    """p(q) = a - b*q, clipped at >= 0 for numerical stability."""
    p = a - b * q
    return np.maximum(p, 0.0)


def revenue(q: np.ndarray, C: float, p: np.ndarray) -> np.ndarray:
    """R(q) = p(q) * min(q, C). q can be vectorized."""
    sold = np.minimum(q, C)
    return p * sold


def profit(q: np.ndarray, C: float, a: float, b: float, c_unit: float, F: float) -> np.ndarray:
    p = linear_price(q, a, b)
    r = revenue(q, C, p)
    return r - c_unit * q - F


# --- Empirical CVaR (Rockafellar–Uryasev, sample-based closed form) ---
def empirical_cvar(losses: np.ndarray, alpha: float) -> float:
    """CVaR_alpha for empirical losses (alpha in [0,1))."""
    if not (0.0 <= alpha < 1.0):
        raise ValueError("alpha must be in [0,1)")
    L = np.sort(losses)  # ascending: worst are at the end if losses are negative? We use losses >= 0 convention
    # Here we assume loss = -profit, so more positive = worse. Sort descending.
    L = np.sort(losses)[::-1]
    m = len(L)
    k = int(np.floor((1 - alpha) * m))
    if k <= 0:
        # Fallback to mean of the worst single sample
        return float(L[0])
    return float(np.mean(L[:k]))


@dataclass
class YearParams:
    a: float  # intercept of price
    b: float  # elasticity wrt q
    C: float  # capacity
    c_unit: float  # unit variable cost
    F: float  # fixed cost


def evaluate_decisions(
    q_grid: np.ndarray,
    scenarios: Iterable[Tuple[float, float, float, float, float]],
    alpha: float = 0.95,
    lam: float = 0.6,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Evaluate each q in q_grid over scenario tuples (a, b, C, c_unit, F).
    Returns (obj, exp_profit, cvar_loss, p5_profit).
    """
    q_grid = np.asarray(q_grid, dtype=float)
    S = list(scenarios)
    S_arr = np.array(S, dtype=float)  # shape: (S, 5)
    a, b, C, c_unit, F = S_arr.T

    obj = np.empty_like(q_grid)
    exp_p = np.empty_like(q_grid)
    cvar = np.empty_like(q_grid)
    p5 = np.empty_like(q_grid)

    for i, q in enumerate(q_grid):
        pi = profit(np.full_like(a, q), C, a, b, c_unit, F)
        losses = -pi
        exp_p[i] = np.mean(pi)
        cvar[i] = empirical_cvar(losses, alpha)
        p5[i] = np.quantile(pi, 0.05)
        obj[i] = exp_p[i] - lam * cvar[i]
    return obj, exp_p, cvar, p5


def simple_rolling_demo(
    T: int = 7,
    q_grid: np.ndarray | None = None,
    alpha: float = 0.95,
    lam: float = 0.6,
    seed: int | None = 0,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    A toy rolling loop:
    - At each year, draw K scenarios around current nominal params
    - Pick q* maximizing E[profit] - lam * CVaR_alpha(loss)
    - Observe realized profit at a single held-out draw and update nominal slightly

    Returns (q_star_seq, profit_realized_seq)
    """
    rng = np.random.default_rng(seed)

    if q_grid is None:
        q_grid = np.linspace(0.0, 1.5, 61)  # in arbitrary units

    # Nominal params (will drift slightly)
    a0, b0, C0, c0, F0 = 2.0, 0.6, 0.9, 0.2, 0.05

    q_star = []
    prof_real = []

    for t in range(T):
        # Draw scenarios (Gaussian jitters)
        K = 200
        a = rng.normal(a0, 0.1, K)
        b = np.abs(rng.normal(b0, 0.05, K))
        C = rng.normal(C0, 0.05, K)
        c_unit = np.abs(rng.normal(c0, 0.02, K))
        F = np.abs(rng.normal(F0, 0.01, K))

        obj, _, _, _ = evaluate_decisions(q_grid, zip(a, b, C, c_unit, F), alpha, lam)
        q_best = float(q_grid[np.argmax(obj)])
        q_star.append(q_best)

        # Realize one outcome and compute realized profit
        a_r, b_r, C_r, c_r, F_r = rng.choice(a), rng.choice(b), rng.choice(C), rng.choice(c_unit), rng.choice(F)
        pi_r = float(profit(np.array([q_best]), float(C_r), float(a_r), float(b_r), float(c_r), float(F_r))[0])
        prof_real.append(pi_r)

        # Mildly update nominal (toy feedback): move a0 down if q is high, adjust capacity drift
        a0 = 0.95 * a0 + 0.05 * (2.0 - 0.2 * q_best)
        C0 = 0.98 * C0 + 0.02 * (0.9 + 0.1 * rng.random())

    return np.array(q_star), np.array(prof_real)


if __name__ == "__main__":
    q, pr = simple_rolling_demo()
    print("q*:", q)
    print("realized profit:", pr)
