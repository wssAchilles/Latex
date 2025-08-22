from __future__ import annotations
from pathlib import Path


def main() -> None:
    # Output path
    project_root = Path(__file__).resolve().parents[1]
    fig_dir = project_root / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / 'model1_stack_area.pdf'

    # Matplotlib implementation (sufficient for stacked area)
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    # Chinese font fallback settings
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    rng = np.random.default_rng(2)
    T = 24
    t = np.linspace(1, T, T)

    # Four crop categories' shares over time (nonnegative, columns sum to 1)
    a = 0.25 + 0.10*np.sin(2*np.pi*t/T + 0.0) + 0.02*rng.standard_normal(T)
    b = 0.25 + 0.08*np.sin(2*np.pi*t/T + 1.2) + 0.02*rng.standard_normal(T)
    c = 0.25 + 0.06*np.sin(2*np.pi*t/T + 2.0) + 0.02*rng.standard_normal(T)
    d = 0.25 + 0.05*np.sin(2*np.pi*t/T + 2.6) + 0.02*rng.standard_normal(T)

    M = np.vstack([a, b, c, d])
    M = np.clip(M, 0.01, None)
    M /= M.sum(axis=0, keepdims=True)  # normalize columns to sum to 1

    labels = ['叶菜类', '茄果类', '豆科类', '根茎类']
    colors = [
        (0.23, 0.49, 0.77),
        (0.93, 0.49, 0.19),
        (0.30, 0.70, 0.30),
        (0.60, 0.45, 0.70),
    ]

    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.stackplot(t, M, labels=labels, colors=colors, alpha=0.9, linewidth=0.5)

    ax.set_xlim(1, T)
    ax.set_ylim(0, 1)
    ax.set_xlabel('月份')
    ax.set_ylabel('作物结构占比')
    ax.set_title('作物结构随时间的堆叠面积图（示意）')
    ax.grid(True, alpha=0.25)

    leg = ax.legend(loc='upper center', ncol=4, frameon=True, bbox_to_anchor=(0.5, -0.12))
    leg.get_frame().set_alpha(0.95)

    fig.tight_layout()
    fig.savefig(out_path, format='pdf', bbox_inches='tight')


if __name__ == '__main__':
    main()
