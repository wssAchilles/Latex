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
    out_path = fig_dir / 'model3_violation_risk_bar.pdf'

    labels = ['确定性', '鲁棒', '滚动+CVaR']
    risks = [0.22, 0.12, 0.07]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.bar(x, risks, color=['#4C72B0', '#C44E52', '#55A868'])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('违约风险')
    ax.set_ylim(0, 0.3)
    ax.set_title('约束违约风险对比')

    for xi, ri in zip(x, risks):
        ax.text(xi, ri+0.01, f"{ri:.2f}", ha='center', va='bottom', fontsize=9)

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
