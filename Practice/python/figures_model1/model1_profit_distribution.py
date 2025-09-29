from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    fig_dir = project_root / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / 'model1_profit_distribution.pdf'

    rng = np.random.default_rng(11)
    # 生成年度净收益样本（万元）：混合正态以体现尾部
    n = 2000
    base = rng.normal(180, 25, size=n)
    tail = rng.normal(120, 10, size=n // 6)
    data = np.concatenate([base, tail])

    fig, ax = plt.subplots(figsize=(9, 4.8))
    counts, bins, patches = ax.hist(data, bins=30, density=True, color='#1f77b4', alpha=0.7, edgecolor='white')

    mean = data.mean()
    p5, p95 = np.percentile(data, [5, 95])

    ax.axvline(mean, color='orange', lw=2, ls='--', label=f'均值 ≈ {mean:.1f}')
    ax.axvspan(p5, p95, color='orange', alpha=0.12, label=f'P5–P95 区间 [{p5:.0f}, {p95:.0f}]')

    ax.set_title('年度净收益分布（示意）')
    ax.set_xlabel('净收益（万元）')
    ax.set_ylabel('密度')
    ax.grid(True, ls='--', alpha=0.3)
    ax.legend(loc='upper right')

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
