from __future__ import annotations
from pathlib import Path
import sys

def main() -> None:
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    project_root = Path(__file__).resolve().parents[1]
    fig_dir = project_root / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / 'model2_gamma_frontier.pdf'

    gammas = np.arange(0, 7)
    worst = 150 + 6*gammas - 0.7*(gammas**2)
    nominal = 180 - 2.2*gammas

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(gammas, worst, marker='o', lw=2.0, color='#d95f02', label='保底收益（最坏）')
    ax.plot(gammas, nominal, marker='s', lw=2.0, color='#1b9e77', label='名义/乐观收益')
    ax.fill_between(gammas, worst, nominal, color='#e6f2ff', alpha=0.6, label='权衡带')

    ax.set_xlabel('鲁棒预算 Γ')
    ax.set_ylabel('年度收益（万元）')
    ax.set_title('鲁棒度—收益前沿（问题二）')
    ax.grid(True, alpha=0.35)
    ax.legend(loc='best')

    for g, w, n in zip(gammas, worst, nominal):
        ax.text(g, w+1.5, f"{w:.0f}", ha='center', fontsize=8)

    fig.tight_layout()
    fig.savefig(out_path, format='pdf', bbox_inches='tight')
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    main()
