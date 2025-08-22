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
    out_path = fig_dir / 'model3_gamma_frontier.pdf'

    gamma = np.linspace(0, 1, 15)
    exp_profit = 1.15e6 - 1.5e5*gamma + 1e4*np.sin(4*gamma)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(gamma, exp_profit/1e6, marker='o')
    ax.set_xlabel('鲁棒预算 Γ')
    ax.set_ylabel('期望收益（百万元）')
    ax.set_title('Γ—收益前沿（示意）')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
