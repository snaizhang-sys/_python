import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 設定中文字型（微軟正黑體適用於 Windows，Heiti TC 適用於 macOS）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 避免負號顯示為方塊

# 建立圖表與軸
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)  # 預留下方空間放置滑桿

# X 軸範圍：0 到 4π
x = np.linspace(0, 4 * np.pi, 1000)

# 初始參數
A_init = 1.0
omega_init = 1.0
phi_init = 0.0

# 計算初始波形
y_sin = A_init * np.sin(omega_init * x + phi_init)
y_cos = A_init * np.cos(omega_init * x + phi_init)

# 繪製兩條曲線
line_sin, = ax.plot(x, y_sin, label='sin', color='#1f77b4', linewidth=2)
line_cos, = ax.plot(x, y_cos, label='cos', color='#ff7f0e', linewidth=2)

# 圖表設定
ax.set_title('正弦與餘弦波形（即時調控）', fontsize=14)
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.set_xlim(0, 4 * np.pi)
ax.set_ylim(-5.5, 5.5)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper right')

# ------- 建立滑桿 -------

# 滑桿顏色
slider_color = 'lightgoldenrodyellow'

# 振幅滑桿
ax_amp = plt.axes([0.15, 0.15, 0.7, 0.03])
slider_amp = Slider(
    ax=ax_amp, label='振幅 A', valmin=0.1, valmax=5.0,
    valinit=A_init, facecolor=slider_color
)

# 頻率滑桿
ax_freq = plt.axes([0.15, 0.10, 0.7, 0.03])
slider_freq = Slider(
    ax=ax_freq, label='頻率 ω', valmin=0.1, valmax=10.0,
    valinit=omega_init, facecolor=slider_color
)

# 相位偏移滑桿
ax_phase = plt.axes([0.15, 0.05, 0.7, 0.03])
slider_phase = Slider(
    ax=ax_phase, label='相位偏移 φ', valmin=0, valmax=2 * np.pi,
    valinit=phi_init, facecolor=slider_color
)


# 更新波形函數
def update(val):
    A = slider_amp.val
    omega = slider_freq.val
    phi = slider_phase.val

    line_sin.set_ydata(A * np.sin(omega * x + phi))
    line_cos.set_ydata(A * np.cos(omega * x + phi))

    fig.canvas.draw_idle()


# 註冊滑桿事件
slider_amp.on_changed(update)
slider_freq.on_changed(update)
slider_phase.on_changed(update)

plt.show()
