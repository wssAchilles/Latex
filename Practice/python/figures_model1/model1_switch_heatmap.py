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
    out_path = fig_dir / 'model1_switch_heatmap.pdf'

    rng = np.random.default_rng(17)
    crops = ['番茄', '黄瓜', '生菜', '辣椒', '茄子']
    n = len(crops)

    # 模拟切换成本（元/亩），对角为0，非对称允许
    cost = rng.integers(80, 260, size=(n, n)).astype(float)
    np.fill_diagonal(cost, 0.0)

    fig, ax = plt.subplots(figsize=(8.6, 6.6))
    im = ax.imshow(cost, cmap='YlOrRd')

    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(crops)
    ax.set_yticklabels(crops)
    ax.set_xlabel('切到 →')
    ax.set_ylabel('从 ←')
    ax.set_title('作物切换成本/频次热力图（示意）')

    # 标注数值
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            ax.text(j, i, f"{cost[i, j]:.0f}", ha='center', va='center', fontsize=8, color='black')

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('切换成本（元/亩）')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
