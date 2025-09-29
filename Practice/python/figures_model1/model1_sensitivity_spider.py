from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def radar_factory(num_vars, frame='circle'):
    # from matplotlib docs, simplified
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    return theta


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    fig_dir = project_root / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / 'model1_sensitivity_spider.pdf'

    labels = ['价格↑', '单产↑', '成本↓', '销量上限↑', '资源瓶颈↓', '切换成本↓']
    N = len(labels)
    theta = radar_factory(N)

    rng = np.random.default_rng(19)
    base = np.clip(rng.normal(0.65, 0.12, size=N), 0.3, 0.95)
    alt = np.clip(base + rng.normal(0.08, 0.07, size=N), 0.2, 1.0)

    fig, ax = plt.subplots(subplot_kw=dict(polar=True), figsize=(7.8, 6.4))

    # 关闭极坐标顶部偏移
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # 设置刻度
    ax.set_thetagrids(theta * 180/np.pi, labels)
    ax.set_ylim(0, 1.0)
    ax.set_rgrids([0.25, 0.5, 0.75, 1.0], angle=90)

    # 闭合多边形：theta 与数据都追加起点
    theta_closed = np.r_[theta, theta[0]]
    ax.plot(theta_closed, np.r_[base, base[0]], color='#1f77b4', lw=2, label='基线')
    ax.fill(theta_closed, np.r_[base, base[0]], color='#1f77b4', alpha=0.15)

    ax.plot(theta_closed, np.r_[alt, alt[0]], color='#ff7f0e', lw=2, label='替代/鲁棒配置')
    ax.fill(theta_closed, np.r_[alt, alt[0]], color='#ff7f0e', alpha=0.12)

    ax.set_title('参数敏感性雷达图（示意）', y=1.08)
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.12))

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
