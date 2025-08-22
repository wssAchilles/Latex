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
    out_path = fig_dir / 'model2_sensitivity_spider_robust.pdf'

    labels = np.array(['价格-茄果', '价格-叶菜', '单产-豆科', '销量上限', '成本-人工', '成本-物料'])
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    det = np.array([0.70, 0.55, 0.40, 0.60, 0.45, 0.50])
    rob = np.array([0.55, 0.48, 0.35, 0.50, 0.42, 0.46])

    det = np.concatenate([det, det[:1]])
    rob = np.concatenate([rob, rob[:1]])

    fig = plt.figure(figsize=(7.0, 6.4))
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, det, 'o-', linewidth=2, label='确定性')
    ax.fill(angles, det, alpha=0.15)
    ax.plot(angles, rob, 'o--', linewidth=2, label='鲁棒')
    ax.fill(angles, rob, alpha=0.15)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title('关键因素对收益波动的敏感性（鲁棒 vs. 确定性）')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))

    fig.tight_layout()
    fig.savefig(out_path, format='pdf', bbox_inches='tight')

if __name__ == '__main__':
    main()
