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
    out_path = fig_dir / 'model3_switch_heatmap.pdf'

    rng = np.random.default_rng(42)
    n_plots, n_crops = 24, 6
    M = rng.uniform(0, 1, size=(n_plots, n_crops))

    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    im = ax.imshow(M, aspect='auto', cmap='viridis')
    ax.set_xlabel('作物')
    ax.set_ylabel('地块')
    fig.colorbar(im, ax=ax, label='切换强度')
    ax.set_title('地块—作物切换热图')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
