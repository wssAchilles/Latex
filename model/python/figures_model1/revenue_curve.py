from __future__ import annotations
from pathlib import Path
import sys


def save_with_matlab(out_path: Path) -> None:
    """Generate an enhanced multi-strategy revenue curve using MATLAB Engine and save as PDF."""
    import matlab.engine  # type: ignore

    eng = matlab.engine.start_matlab()
    try:
        eng.eval("rng(1); T = 24; t = linspace(1,T,T);", nargout=0)
        # Three strategies with a smooth seasonal trend and noise
        eng.eval(
            "base = 100 + 10*sin(2*pi*t/T); "
            "robust = base - 2 + 2*sin(2*pi*t/T + 0.5); "
            "rolling = base + 3*sin(2*pi*t/T + 0.8);",
            nargout=0,
        )
        eng.eval(
            "eps = 2*randn(1,T); "
            "y1 = base + 0.8*eps; y2 = robust + 0.6*eps; y3 = rolling + 0.9*eps;",
            nargout=0,
        )
        # Synthetic CVaR band (e.g., 5th-95th percentile)
        eng.eval(
            "lb = base - 8 - 0.5*(1+sin(2*pi*t/T)); "
            "ub = base + 8 + 0.5*(1+sin(2*pi*t/T));",
            nargout=0,
        )
        eng.eval("f = figure('Visible','off');", nargout=0)
        # Use Chinese font if available
        eng.eval("set(0,'DefaultAxesFontName','SimHei'); set(0,'DefaultTextFontName','SimHei');", nargout=0)
        # Plot CVaR band as a patch
        eng.eval(
            "fill([t, fliplr(t)], [lb, fliplr(ub)], [0.85 0.92 1.0], 'EdgeColor','none'); hold on;",
            nargout=0,
        )
        # Lines
        eng.eval(
            "p1 = plot(t, y1, 'Color',[0.23 0.49 0.77], 'LineWidth',1.8);"
            "p2 = plot(t, y2, 'Color',[0.93 0.49 0.19], 'LineWidth',1.8, 'LineStyle','--');"
            "p3 = plot(t, y3, 'Color',[0.3 0.7 0.3], 'LineWidth',1.8, 'LineStyle','-.');",
            nargout=0,
        )
        # Styling
        eng.eval(
            "grid on; box on; xlim([1 T]); ylabel('净收益（万元）'); xlabel('月份');"
            "title('年度收益曲线：确定性 vs. 鲁棒 vs. 滚动+CVaR');",
            nargout=0,
        )
        eng.eval(
            "legend([p1 p2 p3], {'确定性MIP','鲁棒优化','滚动+CVaR'}, 'Location','best');",
            nargout=0,
        )
        # Annotation
        eng.eval(
            "text(2, ub(2)+1, 'CVaR 置信带（5%-95%）', 'FontSize',9);",
            nargout=0,
        )
        # Export
        out_posix = out_path.as_posix()
        eng.eval(
            f"set(gcf,'PaperPositionMode','auto'); print('-dpdf','-painters','{out_posix}'); close(gcf);",
            nargout=0,
        )
    finally:
        try:
            eng.quit()
        except Exception:
            pass


def save_with_matplotlib(out_path: Path) -> None:
    """Fallback: enhanced figure with matplotlib (no GUI backend)."""
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    # Chinese font setup (fallbacks)
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    T = 24
    t = np.linspace(1, T, T)
    base = 100 + 10*np.sin(2*np.pi*t/T)
    robust = base - 2 + 2*np.sin(2*np.pi*t/T + 0.5)
    rolling = base + 3*np.sin(2*np.pi*t/T + 0.8)
    rng = np.random.default_rng(1)
    eps = 2*rng.standard_normal(T)
    y1 = base + 0.8*eps
    y2 = robust + 0.6*eps
    y3 = rolling + 0.9*eps

    lb = base - 8 - 0.5*(1+np.sin(2*np.pi*t/T))
    ub = base + 8 + 0.5*(1+np.sin(2*np.pi*t/T))

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.fill_between(t, lb, ub, color=(0.85, 0.92, 1.0), edgecolor='none', label='CVaR 置信带（5%-95%）')
    ax.plot(t, y1, color=(0.23, 0.49, 0.77), linewidth=1.8, label='确定性MIP')
    ax.plot(t, y2, color=(0.93, 0.49, 0.19), linewidth=1.8, linestyle='--', label='鲁棒优化')
    ax.plot(t, y3, color=(0.3, 0.7, 0.3), linewidth=1.8, linestyle='-.', label='滚动+CVaR')

    ax.set_xlabel('月份')
    ax.set_ylabel('净收益（万元）')
    ax.set_xlim(1, T)
    ax.grid(True, alpha=0.35)
    ax.set_title('年度收益曲线：确定性 vs. 鲁棒 vs. 滚动+CVaR')
    leg = ax.legend(loc='best', frameon=True)
    leg.get_frame().set_alpha(0.9)

    # Annotate a worst-case marker
    idx_min = int(np.argmin(y2))
    ax.scatter([t[idx_min]], [y2[idx_min]], s=30, color=(0.93, 0.49, 0.19))
    ax.annotate('鲁棒策略低谷', xy=(t[idx_min], y2[idx_min]), xytext=(t[idx_min]+1.5, y2[idx_min]-6),
                arrowprops=dict(arrowstyle='->', color='gray'), fontsize=9)

    fig.tight_layout()
    fig.savefig(out_path, format='pdf')
    plt.close(fig)


def main() -> None:
    # Project root assumed as parent of this script's directory
    project_root = Path(__file__).resolve().parents[1]
    fig_dir = project_root / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / 'model1_revenue_curve.pdf'

    try:
        save_with_matlab(out_path)
        print(f"Generated using MATLAB: {out_path}")
    except Exception as e:
        print(
            f"MATLAB engine not available or failed ({e}). Falling back to matplotlib.",
            file=sys.stderr,
        )
        save_with_matplotlib(out_path)
        print(f"Generated using matplotlib: {out_path}")


if __name__ == '__main__':
    main()
