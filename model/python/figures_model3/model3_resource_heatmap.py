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
    out_path = fig_dir / 'model3_resource_heatmap.pdf'

    rng = np.random.default_rng(9)
    M = rng.uniform(0.3, 1.0, size=(12, 4))

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    im = ax.imshow(M, aspect='auto', cmap='magma', vmin=0, vmax=1)
    ax.set_xlabel('资源')
    ax.set_ylabel('月份')
    fig.colorbar(im, ax=ax, label='利用率')
    ax.set_title('资源使用热图')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
