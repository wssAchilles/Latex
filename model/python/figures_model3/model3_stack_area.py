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
    out_path = fig_dir / 'model3_stack_area.pdf'

    rng = np.random.default_rng(10)
    years = np.arange(1, 8)
    K = 6
    base = rng.uniform(0.1, 1.0, size=(K, len(years)))
    shares = base / base.sum(axis=0, keepdims=True)
    total_area = 1000 + 120*np.sin(0.6*years)
    areas = shares * total_area

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.stackplot(years, areas, labels=[f'C{k+1}' for k in range(K)], alpha=0.9)
    ax.set_xlabel('年份')
    ax.set_ylabel('面积')
    ax.set_title('作物结构演变（示意）')
    ax.legend(ncols=3, fontsize=8, loc='upper right')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
