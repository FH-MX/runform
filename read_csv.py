import pandas as pd   # 表形式データを扱うライブラリを読み込む

# CSVファイルを読み込んで df という変数に入れる（df = DataFrame＝表）
df = pd.read_csv("20260624_224502.csv")

# 先頭5行を表示（どんな列があるか目で確認）
print("=== 先頭5行 ===")
print(df.head())
