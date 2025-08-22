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
    out_path = fig_dir / 'model3_profit_distribution_baseline.pdf'

    rng = np.random.default_rng(123)
    profits = rng.normal(loc=1.2e6, scale=1.8e5, size=1200)

    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.hist(profits, bins=30, color='#4C72B0', alpha=0.8, edgecolor='white')
    ax.set_xlabel('净收益')
    ax.set_ylabel('频数')
    ax.set_title('基线方案收益分布（示意）')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
