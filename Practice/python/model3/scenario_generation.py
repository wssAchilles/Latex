"""
Scenario generation with correlation alignment (PCA) and tail densification.

This module provides a light-weight, dependency-minimal implementation to
- draw Latin Hypercube samples in R^d
- align them to a target Gaussian mean/cov via PCA
- optionally densify the left tail along a target direction (e.g., min-profit)

The code is self-contained (numpy only) and intended for didactic listings.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple
import numpy as np
from numpy.special import erfinv


def _latin_hypercube(n: int, d: int, rng: np.random.Generator) -> np.ndarray:
    """Generate an n x d Latin Hypercube sample in (0,1) with random permutations."""
    U = (rng.random((n, d)) + np.arange(n)[:, None]) / n
    for j in range(d):
        rng.shuffle(U[:, j])
    return U


def _normal_icdf(u: np.ndarray) -> np.ndarray:
    """Approximate standard normal inverse CDF using erfinv."""
    # Clip to avoid +/-inf
    u = np.clip(u, 1e-12, 1 - 1e-12)
    return np.sqrt(2.0) * erfinv(2.0 * u - 1.0)


@dataclass
class PCASampler:
    mu: np.ndarray
    cov: np.ndarray
    m_components: Optional[int] = None  # if None, use all

    def __post_init__(self) -> None:
        d = self.mu.shape[0]
        if self.cov.shape != (d, d):
            raise ValueError("cov shape mismatch")
        # Eigen-decomposition (symmetric PSD)
        vals, vecs = np.linalg.eigh(self.cov)
        # Sort descending
        idx = np.argsort(vals)[::-1]
        self.vals = vals[idx]
        self.vecs = vecs[:, idx]
        self.m = self.m_components or d
        self.m = int(max(1, min(self.m, d)))
        self.Vm = self.vecs[:, : self.m]
        self.Lm_sqrt = np.sqrt(np.maximum(self.vals[: self.m], 0.0))

    def sample(self, Z: np.ndarray) -> np.ndarray:
        """Map Z ~ N(0, I_m) samples to the original space N(mu, cov) via PCA."""
        if Z.ndim != 2 or Z.shape[1] != self.m:
            raise ValueError("Z must be (n, m) with m == selected components")
        return self.mu + Z @ (self.Vm * self.Lm_sqrt).T


def pca_lhs_samples(
    mu: np.ndarray,
    cov: np.ndarray,
    n_samples: int,
    m_components: Optional[int] = None,
    tail_direction: Optional[np.ndarray] = None,
    tail_extra: int = 0,
    seed: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate PCA-aligned Latin Hypercube samples of a Gaussian with optional tail densification.

    Returns (samples, weights) where weights sum to 1.0.

    - If tail_extra > 0 and tail_direction provided, we oversample the left tail by
      drawing additional points biased along the (normalized) tail_direction and then
      reweighting uniformly across all samples.
    """
    rng = np.random.default_rng(seed)
    mu = np.asarray(mu).reshape(-1)
    d = mu.shape[0]
    cov = np.asarray(cov).reshape(d, d)

    pca = PCASampler(mu, cov, m_components)

    # Base LHS in m dimensions -> map to N(0, I_m), then to original space
    U = _latin_hypercube(n_samples, pca.m, rng)
    Z = _normal_icdf(U)
    base = pca.sample(Z)
    samples = [base]

    if tail_extra > 0 and tail_direction is not None:
        v = np.asarray(tail_direction).reshape(-1)
        if v.shape[0] != d:
            raise ValueError("tail_direction dimension mismatch")
        v = v / (np.linalg.norm(v) + 1e-12)
        # Bias: add negative multiples on principal subspace mean-zero coords
        U_tail = _latin_hypercube(tail_extra, pca.m, rng)
        Z_tail = _normal_icdf(U_tail)
        # Project direction onto PCA subspace
        v_m = pca.Vm.T @ v
        v_m = v_m / (np.linalg.norm(v_m) + 1e-12)
        # Shift along negative direction to densify left tail
        scale = 1.5  # moderate bias magnitude
        Z_tail_biased = Z_tail - scale * v_m
        tail = pca.sample(Z_tail_biased)
        samples.append(tail)

    X = np.vstack(samples)
    w = np.ones(X.shape[0], dtype=float)
    w /= w.sum()
    return X, w


if __name__ == "__main__":
    # Minimal demo
    d = 4
    mu = np.array([10.0, 0.08, 1.2, 0.3])
    A = np.array(
        [
            [1.0, 0.2, 0.1, 0.0],
            [0.2, 1.0, 0.3, 0.0],
            [0.1, 0.3, 1.0, 0.2],
            [0.0, 0.0, 0.2, 1.0],
        ]
    )
    cov = A @ A.T * 0.05
    tail_dir = np.array([-1.0, 1.0, -0.5, 0.0])

    X, w = pca_lhs_samples(mu, cov, n_samples=64, m_components=3, tail_direction=tail_dir, tail_extra=16, seed=42)
    print("samples:", X.shape, "weights sum:", w.sum())
