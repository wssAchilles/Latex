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
    out_path = fig_dir / 'model1_resource_heatmap.pdf'

    rng = np.random.default_rng(7)

    seasons = ['春', '夏', '秋', '冬']
    resources = ['温室棚时', '育苗间', '用工时']

    # 模拟季节×资源的利用率（0-1），示意数据
    data = np.clip(rng.normal(0.65, 0.18, size=(len(resources), len(seasons))), 0.1, 0.98)

    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)

    ax.set_xticks(np.arange(len(seasons)))
    ax.set_xticklabels(seasons)
    ax.set_yticks(np.arange(len(resources)))
    ax.set_yticklabels(resources)

    # 在每个格子上标数值
    for i in range(len(resources)):
        for j in range(len(seasons)):
            ax.text(j, i, f"{data[i, j]:.2f}", ha='center', va='center', color='black')

    ax.set_title('季节—设施资源利用热力图（示意，数值为利用率）')

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('利用率')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
