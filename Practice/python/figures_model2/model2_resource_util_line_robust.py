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
    out_path = fig_dir / 'model2_resource_util_line_robust.pdf'

    T = 24
    t = np.arange(1, T+1)
    rng = np.random.default_rng(7)

    util_det = 0.72 + 0.08*np.sin(2*np.pi*t/T + 0.4) + 0.03*rng.standard_normal(T)
    util_rob = 0.68 + 0.05*np.sin(2*np.pi*t/T + 0.2) + 0.02*rng.standard_normal(T)

    util_det = np.clip(util_det, 0.5, 0.95)
    util_rob = np.clip(util_rob, 0.5, 0.95)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(t, util_det, '-o', color='#1f77b4', lw=1.6, ms=3.5, label='确定性')
    ax.plot(t, util_rob, '-s', color='#d95f02', lw=1.6, ms=3.5, label='鲁棒')

    ax.set_xlabel('月份')
    ax.set_ylabel('资源利用率')
    ax.set_title('资源利用率跨期对比（鲁棒 vs. 确定性）')
    ax.set_ylim(0.5, 1.0)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')

    fig.tight_layout()
    fig.savefig(out_path, format='pdf', bbox_inches='tight')

if __name__ == '__main__':
    main()
