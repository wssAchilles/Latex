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
    out_path = fig_dir / 'model1_area_by_crop_bar.pdf'

    rng = np.random.default_rng(23)
    crops = ['番茄', '黄瓜', '生菜', '辣椒', '茄子']
    areas = rng.integers(120, 380, size=len(crops))  # 亩

    x = np.arange(len(crops))

    fig, ax = plt.subplots(figsize=(9, 4.8))
    bars = ax.bar(x, areas, color='#9467bd', alpha=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels(crops)
    ax.set_ylabel('面积（亩）')
    ax.set_title('主要作物总种植面积对比（示意）')
    ax.grid(axis='y', ls='--', alpha=0.3)

    for i, b in enumerate(bars):
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 6, f"{areas[i]}", ha='center', va='bottom', fontsize=9)

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
