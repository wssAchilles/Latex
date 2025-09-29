from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def _style_polar(ax):
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1.0)
    ax.grid(True, color='0.85', lw=0.8)
    if 'polar' in ax.spines:
        ax.spines['polar'].set_color('#999999')
        ax.spines['polar'].set_linewidth(1.0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8'], fontsize=8, color='0.5')
    ax.set_rlabel_position(22.5)


def draw_radar(ax, labels, values, color, label, annotate=False):
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    vals = list(values) + [values[0]]
    angs = angles + [angles[0]]
    ax.plot(angs, vals, color=color, lw=2, marker='o', markersize=4, label=label)
    ax.fill(angs, vals, color=color, alpha=0.2)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    if annotate:
        for ang, val in zip(angles, values):
            ax.text(ang, min(val + 0.05, 0.98), f'{val:.2f}', ha='center', va='center', fontsize=8, color=color)


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    fig_dir = project_root / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)

    labels = ['价格\n弹性', '容量', '单产\n方差', '切换\n惩罚', '单位\n成本']
    vals_base = [0.85, 0.9, 0.6, 0.35, 0.5]
    vals_rob = [0.6, 0.65, 0.5, 0.45, 0.4]

    # Side-by-side comparison
    fig, axes = plt.subplots(1, 2, subplot_kw=dict(polar=True), figsize=(10.2, 5.2))
    for ax in axes:
        _style_polar(ax)
    draw_radar(axes[0], labels, vals_base, '#4C72B0', '基线', annotate=False)
    axes[0].set_xticklabels(labels, fontsize=11)
    axes[0].set_title('敏感性（基线）', pad=16, fontsize=12, fontweight='bold')

    draw_radar(axes[1], labels, vals_rob, '#55A868', '滚动+CVaR', annotate=False)
    axes[1].set_xticklabels(labels, fontsize=11)
    axes[1].set_title('敏感性（滚动+CVaR）', pad=16, fontsize=12, fontweight='bold')

    fig.tight_layout()
    fig.savefig(fig_dir / 'model3_sensitivity_spider_compare_side_by_side.pdf', bbox_inches='tight')

    # Overlay comparison (two series in one plot)
    fig2 = plt.figure(figsize=(6.8, 5.2))
    ax = plt.subplot(111, polar=True)
    _style_polar(ax)
    draw_radar(ax, labels, vals_base, '#4C72B0', '基线', annotate=False)
    draw_radar(ax, labels, vals_rob, '#55A868', '滚动+CVaR', annotate=False)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_title('敏感性对比（基线 vs 滚动+CVaR）', pad=16, fontsize=12, fontweight='bold')
    leg = ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1.0), borderaxespad=0.0, frameon=True)
    leg.get_frame().set_alpha(0.9)
    plt.subplots_adjust(right=0.82, top=0.9)
    fig2.savefig(fig_dir / 'model3_sensitivity_spider_compare_overlay.pdf', bbox_inches='tight')


if __name__ == '__main__':
    main()
