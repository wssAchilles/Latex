# Helper for both spider charts, not directly called by LaTeX
from __future__ import annotations
from typing import List
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def radar(ax, labels: List[str], values: List[float], color: str, label: str):
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    vals = list(values) + [values[0]]
    angs = angles + [angles[0]]
    ax.plot(angs, vals, color=color, lw=2, label=label)
    ax.fill(angs, vals, color=color, alpha=0.15)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
