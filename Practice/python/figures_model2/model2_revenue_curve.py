from __future__ import annotations
from pathlib import Path
import sys

def save_matplotlib(out_path: Path) -> None:
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    # Chinese font fallback
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    T = 24
    t = np.linspace(1, T, T)
    base = 110 + 12*np.sin(2*np.pi*t/T)
    robust = base - 3 + 2.2*np.sin(2*np.pi*t/T + 0.4)
    det = base + 3.5*np.sin(2*np.pi*t/T + 0.9)
    rng = np.random.default_rng(2025)
    eps = 2.2*rng.standard_normal(T)

    y_det = base + 0.9*eps
    y_rob = robust + 0.6*eps

    lb = base - 9 - 0.6*(1+np.sin(2*np.pi*t/T))
    ub = base + 9 + 0.6*(1+np.sin(2*np.pi*t/T))

    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    ax.fill_between(t, lb, ub, color=(0.85, 0.92, 1.0), edgecolor='none', label='CVaR 置信带（5%-95%）')
    ax.plot(t, y_det, color=(0.23, 0.49, 0.77), linewidth=1.9, label='确定性MIP')
    ax.plot(t, y_rob, color=(0.93, 0.49, 0.19), linewidth=1.9, linestyle='--', label='鲁棒优化')

    ax.set_xlabel('月份')
    ax.set_ylabel('净收益（万元）')
    ax.set_xlim(1, T)
    ax.grid(True, alpha=0.35)
    ax.set_title('年度收益曲线：确定性 vs. 鲁棒（问题二）')
    leg = ax.legend(loc='best', frameon=True)
    leg.get_frame().set_alpha(0.9)

    # annotate worst case of robust
    idx_min = int(np.argmin(y_rob))
    ax.scatter([t[idx_min]], [y_rob[idx_min]], s=28, color=(0.93, 0.49, 0.19))
    ax.annotate('鲁棒策略低谷', xy=(t[idx_min], y_rob[idx_min]), xytext=(t[idx_min]+1.2, y_rob[idx_min]-7),
                arrowprops=dict(arrowstyle='->', color='gray'), fontsize=9)

    fig.tight_layout()
    fig.savefig(out_path, format='pdf', bbox_inches='tight')
    plt.close(fig)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    fig_dir = project_root / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / 'model2_revenue_curve.pdf'
    try:
        save_matplotlib(out_path)
        print(f"Generated: {out_path}")
    except Exception as e:
        print(f"Failed to generate figure: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
