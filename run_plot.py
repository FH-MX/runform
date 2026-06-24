# 加速度の波形をプロットする

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("20260624_224502.csv")   # ←自分のファイル名に変える
t = df["time_ms"] / 1000.0                 # 秒に変換

# --- 加速度3軸を縦に3段で並べる ---
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)  # 3段・X軸共有
for ax, col in zip(axes, ["ax_g", "ay_g", "az_g"]):
    ax.plot(t, df[col], lw=0.8)   # 波形を描く
    ax.set_ylabel(col)            # 縦軸ラベル
    ax.grid(alpha=0.3)            # うすいグリッド
axes[-1].set_xlabel("time (s)")   # 一番下だけ横軸ラベル
plt.tight_layout()

plt.show()