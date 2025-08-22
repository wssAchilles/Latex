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
    out_path = fig_dir / 'model3_regret_curve.pdf'

    x = np.linspace(0, 1, 50)
    regret = 2.0*np.exp(-3*x) + 0.1

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(x, regret, color='#C44E52')
    ax.set_xlabel('保守度')
    ax.set_ylabel('后悔值')
    ax.set_title('后悔值曲线（示意）')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
