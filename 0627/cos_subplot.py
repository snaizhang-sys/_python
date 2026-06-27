# 步驟 1:匯入 numpy,並取別名 np
import numpy as np

# 步驟 2:匯入 matplotlib.pyplot,並取別名 plt
import matplotlib.pyplot as plt

# 步驟 3:用 np.arange() 產生 0 到 4(不含 4)、間隔 0.2 的陣列,存入 x
x = np.arange(0, 4, 0.2)

# 步驟 4:計算 y1 = cos(pi * x)(用 np.cos 與 np.pi)
y1 = np.cos(np.pi * x)

# 步驟 5:計算 y2 = cos(2 * pi * x)
y2 = np.cos(2 * np.pi * x)

# 步驟 6:用 subplot 把版面切成 1 列 2 欄,選第 1 格(左圖)
plt.subplot(1, 2, 1)

# 步驟 7:畫出 x 與 y1,使用綠色實線
plt.plot(x, y1, 'g-')

# 步驟 8:用 subplot 選第 2 格(右圖)
plt.subplot(1, 2, 2)

# 步驟 9:畫出 x 與 y2,使用洋紅色點線
plt.plot(x, y2, 'm:')

# 步驟 10:顯示圖形
plt.show()
