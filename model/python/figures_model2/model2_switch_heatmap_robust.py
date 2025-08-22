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
    out_path = fig_dir / 'model2_switch_heatmap_robust.pdf'

    rng = np.random.default_rng(17)
    crops = ['番茄', '黄瓜', '生菜', '辣椒', '茄子']
    n = len(crops)

    # 模拟鲁棒方案下的切换频次矩阵（更稀疏/更低频）
    freq = rng.poisson(2, size=(n, n)).astype(float)
    np.fill_diagonal(freq, 0.0)
    freq = np.minimum(freq, 6)

    fig, ax = plt.subplots(figsize=(8.6, 6.6))
    im = ax.imshow(freq, cmap='Greens')

    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(crops)
    ax.set_yticklabels(crops)
    ax.set_xlabel('切到 →')
    ax.set_ylabel('从 ←')
    ax.set_title('鲁棒方案切换频次热力图（示意）')

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            ax.text(j, i, f"{freq[i, j]:.0f}", ha='center', va='center', fontsize=8, color='black')

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('切换频次（次）')

    fig.tight_layout()
    fig.savefig(out_path, format='pdf', bbox_inches='tight')

if __name__ == '__main__':
    main()
