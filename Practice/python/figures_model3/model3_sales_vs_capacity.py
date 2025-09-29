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
    out_path = fig_dir / 'model3_sales_vs_capacity.pdf'

    C = 180.0
    q = np.linspace(0, 250, 400)
    s = np.minimum(q, C)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(q, s, label='s(q)=min(q,C)')
    ax.axvline(C, ls='--', c='r', lw=1, label='容量 C')
    ax.set_xlabel('有效供给 q')
    ax.set_ylabel('销量 s(q)')
    ax.set_title('销量—产能配比示意')
    ax.legend()

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
