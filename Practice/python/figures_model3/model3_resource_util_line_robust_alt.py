# Optional alternative style for internal comparison; not used by LaTeX
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
    out_path = fig_dir / 'model3_resource_util_line_robust_alt.pdf'

    years = np.arange(1, 8)
    util_robust = 0.78 + 0.07*np.sin(0.9*years)
    util_roll = 0.72 + 0.06*np.sin(0.9*years + 0.7)

    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    ax.plot(years, util_robust, marker='o', label='鲁棒')
    ax.plot(years, util_roll, marker='s', label='滚动+CVaR')
    ax.set_xlabel('年份')
    ax.set_ylabel('利用率')
    ax.set_ylim(0, 1.05)
    ax.set_title('关键资源利用率对比（可选样式）')
    ax.legend()

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
