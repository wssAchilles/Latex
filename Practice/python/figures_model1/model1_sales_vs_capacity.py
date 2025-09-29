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
    out_path = fig_dir / 'model1_sales_vs_capacity.pdf'

    rng = np.random.default_rng(13)
    crops = ['番茄', '黄瓜', '生菜', '辣椒', '茄子']
    n = len(crops)

    capacity = rng.integers(40, 90, size=n)  # 销量上限（吨）
    sales = (capacity * rng.uniform(0.6, 1.05, size=n)).clip(0, None)

    x = np.arange(n)
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.bar(x - width/2, capacity, width, label='销量上限 (吨)', color='#7f7f7f')
    ax.bar(x + width/2, sales, width, label='实际销量 (吨)', color='#2ca02c', alpha=0.9)

    ax.set_xticks(x)
    ax.set_xticklabels(crops)
    ax.set_ylabel('吨')
    ax.set_title('销量与销量上限对照（示意）')
    ax.grid(axis='y', ls='--', alpha=0.3)
    ax.legend(loc='upper left')

    for i, (c, s) in enumerate(zip(capacity, sales)):
        gap = c - s
        ax.text(i + width/2, s + 1.5, f"Gap {gap:.1f}", ha='center', va='bottom', fontsize=9, color='#444')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
