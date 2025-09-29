from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    fig_dir = project_root / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / 'model3_revenue_curve.pdf'

    a, b, C = 10.0, 0.02, 180.0
    q = np.linspace(0, 250, 400)
    p = np.maximum(a - b*q, 0.5)
    s = np.minimum(q, C)
    R = p * s

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(q, R, label='R(q)=p(q)·min(q,C)')
    ax.axvline(C, ls='--', c='r', lw=1, label='容量 C')
    ax.set_xlabel('有效供给 q')
    ax.set_ylabel('收入 R')
    ax.set_title('收入—供给曲线（带容量上限）')
    ax.legend()

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
