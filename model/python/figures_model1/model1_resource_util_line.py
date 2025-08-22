from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    fig_dir = project_root / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / 'model1_resource_util_line.pdf'

    rng = np.random.default_rng(7)
    T = 24
    t = np.arange(1, T + 1)
    base = 0.72 + 0.10 * np.sin(2 * np.pi * t / 12.0)
    noise = 0.03 * rng.standard_normal(T)
    util = np.clip(base + noise, 0.45, 0.98)

    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.plot(t, util * 100, color='#2ca02c', marker='o', lw=2, label='资源利用率')
    ax.axhline(85, color='red', ls='--', lw=1, alpha=0.6, label='建议上限 85%')
    ax.set_xlabel('期次')
    ax.set_ylabel('利用率 (%)')
    ax.set_title('资源利用率跨期折线图（示意）')
    ax.set_xticks(t)
    ax.grid(True, ls='--', alpha=0.3)
    ax.legend(loc='upper right')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
