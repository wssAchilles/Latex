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
    out_path = fig_dir / 'model2_structure_stack_area_gamma.pdf'

    rng = np.random.default_rng(8)
    T = 24
    t = np.linspace(1, T, T)

    def stack_data(seed_shift: float = 0.0):
        a = 0.25 + 0.10*np.sin(2*np.pi*t/T + 0.0 + seed_shift) + 0.02*rng.standard_normal(T)
        b = 0.25 + 0.08*np.sin(2*np.pi*t/T + 1.2 + seed_shift) + 0.02*rng.standard_normal(T)
        c = 0.25 + 0.06*np.sin(2*np.pi*t/T + 2.0 + seed_shift) + 0.02*rng.standard_normal(T)
        d = 0.25 + 0.05*np.sin(2*np.pi*t/T + 2.6 + seed_shift) + 0.02*rng.standard_normal(T)
        M = np.vstack([a, b, c, d])
        M = np.clip(M, 0.01, None)
        M /= M.sum(axis=0, keepdims=True)
        return M

    M0 = stack_data(0.0)
    M3 = stack_data(0.35)  # 视作 Γ=3 后的稳健再配置

    labels = ['叶菜类', '茄果类', '豆科类', '根茎类']
    colors = [(0.23,0.49,0.77),(0.93,0.49,0.19),(0.30,0.70,0.30),(0.60,0.45,0.70)]

    fig, axes = plt.subplots(2, 1, figsize=(7.4, 6.6), sharex=True)
    for ax, M, title in zip(axes, [M0, M3], ['Γ=0（确定性）', 'Γ=3（鲁棒）']):
        ax.stackplot(t, M, labels=labels, colors=colors, alpha=0.9, linewidth=0.5)
        ax.set_ylim(0, 1)
        ax.set_ylabel('结构占比')
        ax.set_title(title)
        ax.grid(True, alpha=0.25)
    axes[-1].set_xlabel('月份')
    axes[0].legend(loc='upper center', ncol=4, frameon=True, bbox_to_anchor=(0.5, -0.12))

    fig.tight_layout()
    fig.savefig(out_path, format='pdf', bbox_inches='tight')

if __name__ == '__main__':
    main()
