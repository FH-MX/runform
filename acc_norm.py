import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("20260624_224502.csv")
# 合成加速度（3軸のベクトルの大きさ）を新しい列として追加
df["acc_norm"] = np.sqrt(df["ax_g"]**2 + df["ay_g"]**2 + df["az_g"]**2)

# 確認
print(df["acc_norm"].describe())   # 平均・最大などを見る

# --- 加速度の波形をプロットする ---
t = df["time_ms"] / 1000.0
plt.figure(figsize=(12, 4))
plt.plot(t, df["acc_norm"], lw=0.8)
plt.axhline(1.0, color="gray", ls="--", label="1g (静止時の基準)")  # 基準線
plt.xlabel("time (s)")
plt.ylabel("acc_norm (g)")
plt.legend()
plt.grid(alpha=0.3)
plt.show()