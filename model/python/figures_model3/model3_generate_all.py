#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate all model 3 figures into the project figures/ directory.
Figures list (as referenced in mainmatter/03-model_3.tex):
- model3_revenue_curve.pdf
- model3_sales_vs_capacity.pdf
- model3_profit_distribution_baseline.pdf
- model3_sensitivity_spider_baseline.pdf
- model3_switch_heatmap.pdf
- model3_gamma_frontier.pdf
- model3_regret_curve.pdf
- model3_stack_area.pdf
- model3_resource_util_line_robust.pdf
- model3_revenue_curve_capped.pdf
- model3_sensitivity_spider_robust.pdf
- model3_violation_risk_bar.pdf
- model3_yield_bar.pdf
- model3_resource_heatmap.pdf

The figures are illustrative using synthetic data consistent with the narrative.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt

# Matplotlib global style
plt.rcParams.update({
    'figure.dpi': 140,
    'savefig.dpi': 300,
    'font.size': 10,
    'axes.grid': True,
    'grid.alpha': 0.25,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Resolve output directory figures/ relative to repo root
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]
FIG_DIR = PROJECT_ROOT / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)


def savefig(name: str):
    path = FIG_DIR / name
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"[saved] {path}")


def revenue_curve():
    # p(q) = a - b q, R(q) = p(q)*min(q, C)
    a, b, C = 10.0, 0.02, 180.0
    q = np.linspace(0, 250, 400)
    p = np.maximum(a - b*q, 0.5)
    s = np.minimum(q, C)
    R = p * s

    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(q, R, label='R(q)=p(q)·min(q,C)')
    ax.axvline(C, ls='--', c='r', lw=1, label='Capacity C')
    ax.set_xlabel('q (effective supply)')
    ax.set_ylabel('Revenue R')
    ax.set_title('Revenue vs Supply with Capacity')
    ax.legend()
    savefig('model3_revenue_curve.pdf')


def sales_vs_capacity():
    C = 180.0
    q = np.linspace(0, 250, 400)
    s = np.minimum(q, C)
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(q, s, label='Sales s(q)=min(q,C)')
    ax.axvline(C, ls='--', c='r', lw=1, label='Capacity C')
    ax.set_xlabel('q (effective supply)')
    ax.set_ylabel('Sales s(q)')
    ax.set_title('Sales vs Capacity')
    ax.legend()
    savefig('model3_sales_vs_capacity.pdf')


def profit_distribution_baseline():
    # Synthetic baseline profit distribution
    rng = np.random.default_rng(123)
    profits = rng.normal(loc=1.2e6, scale=1.8e5, size=1000)
    fig, ax = plt.subplots(figsize=(5.0, 3.2))
    ax.hist(profits, bins=30, color='#4C72B0', alpha=0.85)
    ax.set_xlabel('Profit')
    ax.set_ylabel('Frequency')
    ax.set_title('Baseline Profit Distribution')
    savefig('model3_profit_distribution_baseline.pdf')


def radar(ax, labels: List[str], values: List[float], color: str, label: str):
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    vals = values + values[:1]
    angs = angles + angles[:1]
    ax.plot(angs, vals, color=color, lw=2, label=label)
    ax.fill(angs, vals, color=color, alpha=0.15)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    ax.set_ylim(0, max(1.0, max(values)*1.2))


def sensitivity_spider_baseline():
    labels = ['Price elasticity', 'Capacity', 'Yield var', 'Switch penalty', 'Unit cost']
    vals = [0.85, 0.9, 0.6, 0.35, 0.5]
    fig = plt.figure(figsize=(5.0, 5.0))
    ax = plt.subplot(111, polar=True)
    radar(ax, labels, vals, '#4C72B0', 'Baseline')
    ax.set_title('Sensitivity Spider (Baseline)')
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1))
    savefig('model3_sensitivity_spider_baseline.pdf')


def switch_heatmap():
    # Heatmap of switching intensity over plots x crops
    rng = np.random.default_rng(42)
    n_plots, n_crops = 24, 6
    M = rng.uniform(0, 1, size=(n_plots, n_crops))
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    im = ax.imshow(M, aspect='auto', cmap='viridis')
    ax.set_xlabel('Crops')
    ax.set_ylabel('Plots')
    fig.colorbar(im, ax=ax, label='Switch intensity')
    ax.set_title('Switch Heatmap')
    savefig('model3_switch_heatmap.pdf')


def gamma_frontier():
    # Tradeoff curve: expected profit vs robustness budget
    gamma = np.linspace(0, 1, 15)
    exp_profit = 1.15e6 - 1.5e5*gamma + 1e4*np.sin(4*gamma)
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(gamma, exp_profit/1e6, marker='o')
    ax.set_xlabel('Robustness budget Γ')
    ax.set_ylabel('Expected profit (million)')
    ax.set_title('Γ-Frontier')
    savefig('model3_gamma_frontier.pdf')


def regret_curve():
    x = np.linspace(0, 1, 50)
    regret = 2.0*np.exp(-3*x) + 0.1
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(x, regret, color='#C44E52')
    ax.set_xlabel('Conservativeness')
    ax.set_ylabel('Regret')
    ax.set_title('Regret Curve')
    savefig('model3_regret_curve.pdf')


def stack_area():
    # Area by crops over time (years)
    rng = np.random.default_rng(10)
    years = np.arange(1, 8)
    K = 6
    base = rng.uniform(0.1, 1.0, size=(K, len(years)))
    shares = base / base.sum(axis=0, keepdims=True)
    total_area = 1000 + 120*np.sin(0.6*years)
    areas = shares * total_area
    fig, ax = plt.subplots(figsize=(5.8, 3.4))
    ax.stackplot(years, areas, labels=[f'C{k+1}' for k in range(K)], alpha=0.9)
    ax.set_xlabel('Year')
    ax.set_ylabel('Area')
    ax.set_title('Structure Evolution')
    ax.legend(ncols=3, fontsize=8, loc='upper right')
    savefig('model3_stack_area.pdf')


def resource_util_line_robust():
    years = np.arange(1, 8)
    util_robust = 0.75 + 0.1*np.sin(0.7*years)
    util_roll = 0.7 + 0.08*np.sin(0.7*years + 0.6)
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.plot(years, util_robust, marker='o', label='Robust')
    ax.plot(years, util_roll, marker='s', label='Rolling+CVaR')
    ax.set_xlabel('Year')
    ax.set_ylabel('Utilization')
    ax.set_ylim(0, 1.05)
    ax.set_title('Resource Utilization')
    ax.legend()
    savefig('model3_resource_util_line_robust.pdf')


def revenue_curve_capped():
    # Show kink at capacity more explicitly with two regimes
    a, b, C = 10.0, 0.02, 160.0
    q = np.linspace(0, 240, 400)
    p = np.maximum(a - b*q, 0.5)
    s = np.minimum(q, C)
    R = p * s
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(q[q<=C], R[q<=C], color='#4C72B0', label='q <= C')
    ax.plot(q[q>C], R[q>C], color='#55A868', label='q > C')
    ax.axvline(C, ls='--', c='r', lw=1, label='Capacity C')
    ax.set_xlabel('q (effective supply)')
    ax.set_ylabel('Revenue R')
    ax.set_title('Revenue Curve (Capped)')
    ax.legend()
    savefig('model3_revenue_curve_capped.pdf')


def sensitivity_spider_robust():
    labels = ['Price elasticity', 'Capacity', 'Yield var', 'Switch penalty', 'Unit cost']
    vals_robust = [0.6, 0.65, 0.5, 0.45, 0.4]
    fig = plt.figure(figsize=(5.0, 5.0))
    ax = plt.subplot(111, polar=True)
    radar(ax, labels, vals_robust, '#55A868', 'Rolling+CVaR')
    ax.set_title('Sensitivity Spider (Rolling+CVaR)')
    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1))
    savefig('model3_sensitivity_spider_robust.pdf')


def violation_risk_bar():
    labels = ['Deterministic', 'Robust', 'Rolling+CVaR']
    risks = [0.22, 0.12, 0.07]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(5.0, 3.2))
    ax.bar(x, risks, color=['#4C72B0', '#C44E52', '#55A868'])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Violation risk')
    ax.set_ylim(0, 0.3)
    ax.set_title('Constraint Violation Risk')
    for xi, ri in zip(x, risks):
        ax.text(xi, ri+0.01, f"{ri:.2f}", ha='center', va='bottom')
    savefig('model3_violation_risk_bar.pdf')


def yield_bar():
    rng = np.random.default_rng(7)
    crops = [f'C{k+1}' for k in range(6)]
    yields = rng.normal(6.0, 0.8, size=len(crops))
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.bar(crops, yields, color='#4C72B0', alpha=0.9)
    ax.set_xlabel('Crop')
    ax.set_ylabel('Yield (t/ha)')
    ax.set_title('Yield Profile')
    savefig('model3_yield_bar.pdf')


def resource_heatmap():
    rng = np.random.default_rng(9)
    # e.g., 12 months x 4 resources utilization heatmap
    M = rng.uniform(0.3, 1.0, size=(12, 4))
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    im = ax.imshow(M, aspect='auto', cmap='magma', vmin=0, vmax=1)
    ax.set_xlabel('Resources')
    ax.set_ylabel('Months')
    fig.colorbar(im, ax=ax, label='Utilization')
    ax.set_title('Resource Heatmap')
    savefig('model3_resource_heatmap.pdf')


def main():
    revenue_curve()
    sales_vs_capacity()
    profit_distribution_baseline()
    sensitivity_spider_baseline()
    switch_heatmap()
    gamma_frontier()
    regret_curve()
    stack_area()
    resource_util_line_robust()
    revenue_curve_capped()
    sensitivity_spider_robust()
    violation_risk_bar()
    yield_bar()
    resource_heatmap()
    print(f"All model3 figures saved to: {FIG_DIR}")


if __name__ == '__main__':
    main()
