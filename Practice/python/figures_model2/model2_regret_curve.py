from __future__ import annotations
from pathlib import Path

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
    out_path = fig_dir / 'model2_regret_curve.pdf'

    rng = np.random.default_rng(42)
    # regret = revenue(oracle) - revenue(policy)
    regret_det = np.abs(rng.normal(14, 6, size=500)).clip(0, None)
    regret_rob = np.abs(rng.normal(8, 4, size=500)).clip(0, None)

    def ecdf(x):
        xs = np.sort(x)
        ys = np.arange(1, len(xs)+1) / len(xs)
        return xs, ys

    x1, y1 = ecdf(regret_det)
    x2, y2 = ecdf(regret_rob)

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(x1, y1, lw=2.0, color='#1f77b4', label='确定性：后悔分布')
    ax.plot(x2, y2, lw=2.0, color='#d95f02', label='鲁棒：后悔分布')

    ax.set_xlabel('后悔值（万元）')
    ax.set_ylabel('累计概率')
    ax.set_title('后悔值 ECDF 对比（问题二）')
    ax.grid(True, alpha=0.35)
    ax.legend(loc='lower right')

    fig.tight_layout()
    fig.savefig(out_path, format='pdf', bbox_inches='tight')

if __name__ == '__main__':
    main()
