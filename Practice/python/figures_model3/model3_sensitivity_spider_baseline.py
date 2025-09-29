from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def _radar(ax, labels, values, color, label):
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    vals = list(values) + [values[0]]
    angs = angles + [angles[0]]
    ax.plot(angs, vals, color=color, lw=2, marker='o', markersize=4, label=label)
    ax.fill(angs, vals, color=color, alpha=0.2)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    # numeric annotations near vertices for readability
    for ang, val in zip(angles, values):
        # Skip top-vertex annotation to avoid any chance of title overlap
        if abs(ang) < 1e-6:
            continue
        r = min(val + 0.05, 0.98)
        ax.text(ang, r, f'{val:.2f}', ha='center', va='center', fontsize=8, color=color)


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    fig_dir = project_root / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / 'model3_sensitivity_spider_baseline.pdf'

    labels = ['价格弹性', '容量', '单产\n方差', '切换\n惩罚', '单位\n成本']
    vals = [0.85, 0.9, 0.6, 0.35, 0.5]

    fig = plt.figure(figsize=(6.0, 5.2))
    ax = plt.subplot(111, polar=True)
    # Consistent orientation & limits
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1.0)
    # Softer grid and clearer border
    ax.grid(True, color='0.85', lw=0.8)
    if 'polar' in ax.spines:
        ax.spines['polar'].set_color('#999999')
        ax.spines['polar'].set_linewidth(1.0)
    # radial ticks
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8'], fontsize=8, color='0.5')
    ax.set_rlabel_position(22.5)

    _radar(ax, labels, vals, '#4C72B0', '基线')
    ax.set_xticklabels(labels, fontsize=10)
    ax.tick_params(axis='x', pad=-8)
    ax.set_title('敏感性（基线）', pad=36, fontsize=12, fontweight='bold')

    # Legend outside on the right
    leg = ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1.0), borderaxespad=0.0, frameon=True)
    leg.get_frame().set_alpha(0.9)

    plt.subplots_adjust(right=0.82, top=0.85)
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
