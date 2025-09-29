from __future__ import annotations
from pathlib import Path

def main() -> None:
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    project_root = Path(__file__).resolve().parents[1]
    fig_dir = project_root / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / 'model2_violation_risk_bar.pdf'

    categories = ['销量约束', '资源瓶颈', '轮作/重茬', '适宜性']
    det = np.array([0.18, 0.12, 0.08, 0.05])  # 违约概率（示意）
    rob = np.array([0.07, 0.05, 0.04, 0.03])

    x = np.arange(len(categories))
    width = 0.36

    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.bar(x - width/2, det, width=width, label='确定性', color='#1f77b4')
    ax.bar(x + width/2, rob, width=width, label='鲁棒', color='#d95f02')

    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel('违约概率（模拟）')
    ax.set_title('约束违约风险对比：确定性 vs. 鲁棒')
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend(loc='upper right')

    for i, v in enumerate(det):
        ax.text(x[i]-width/2, v+0.01, f"{v:.2f}", ha='center', fontsize=8)
    for i, v in enumerate(rob):
        ax.text(x[i]+width/2, v+0.01, f"{v:.2f}", ha='center', fontsize=8)

    fig.tight_layout()
    fig.savefig(out_path, format='pdf', bbox_inches='tight')

if __name__ == '__main__':
    main()
