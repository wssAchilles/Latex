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
    out_path = fig_dir / 'model1_yield_bar.pdf'

    rng = np.random.default_rng(3)

    crops = ['番茄', '黄瓜', '生菜', '辣椒', '茄子']
    n = len(crops)

    # 模拟数据（示意）：单产 kg/亩，单位净利 元/亩
    yield_kg_per_mu = rng.normal(2500, 200, size=n).clip(1800, 3200)
    unit_profit = rng.normal(1800, 300, size=n).clip(1000, 2600)

    x = np.arange(n)
    width = 0.35

    fig, ax1 = plt.subplots(figsize=(9, 5.2))
    ax2 = ax1.twinx()

    bars1 = ax1.bar(x - width/2, yield_kg_per_mu, width, label='单产 (kg/亩)', color='#1f77b4')
    bars2 = ax2.bar(x + width/2, unit_profit, width, label='单位净利 (元/亩)', color='#ff7f0e', alpha=0.85)

    ax1.set_xticks(x)
    ax1.set_xticklabels(crops)

    ax1.set_ylabel('单产 (kg/亩)')
    ax2.set_ylabel('单位净利 (元/亩)')

    ax1.set_title('主要作物单产与单位净利对比（示意）')

    # 合并图例
    handles = [bars1, bars2]
    labels = [h.get_label() for h in handles]
    ax1.legend(handles, labels, loc='upper left')

    ax1.grid(axis='y', linestyle='--', alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
