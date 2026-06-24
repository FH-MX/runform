import pandas as pd

df = df = pd.read_csv("20260624_224502.csv") 

# 1  基本統計
print("=== 加速度３軸 ===")
print(df[["ax_g", "ay_g", "az_g"]].describe())

# 2 サンプリングレート
dt = df['time_ms'].diff().dropna()  # 差分を計算して NaN を削除

# 中央値を使い計算(外れ値に影響されないようにする)
dt_median = dt.median()
print("=== サンプリングレート ===")
print(f"サンプリング間隔の中央値: {dt_median:.1f} ms")
print(f"実行サンプリングレート: {1000/dt_median:.2f} Hz")

# 3 dtの分布
# 5/25/50/75/95%点を見る。ばらけ方が分かる
q = dt.quantile([0.05, 0.25, 0.5, 0.75, 0.95])
print("\n=== dt分位点 (ms) ===")
print(q.round(0))