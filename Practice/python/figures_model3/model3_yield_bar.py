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
    out_path = fig_dir / 'model3_yield_bar.pdf'

    rng = np.random.default_rng(7)
    crops = [f'C{k+1}' for k in range(6)]
    yields = rng.normal(6.0, 0.8, size=len(crops))

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(crops, yields, color='#4C72B0', alpha=0.9)
    ax.set_xlabel('作物')
    ax.set_ylabel('单产（t/ha）')
    ax.set_title('单产剖面（示意）')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
