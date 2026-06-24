# RunForm
足首に装着したIMUセンサ（ESP32 + MPU-6050）からの信号(csv)の計算用


## システム構成

```
[MPU-6050] --I2C--> [ESP32] --BLE(Notify)--> [Android]--> [PC]
   6軸IMU            送信側                      受信
```

| 層 | 使用技術 |
| --- | --- |
| センサ | MPU-6050（6軸: 加速度3軸 + ジャイロ3軸）、±8g / ±1000dps |
| マイコン | ESP32（Arduino / C++）、BLE Notifyで12バイト/回を送信 |
| 解析 | Python（pandas / numpy / matplotlib） |


### 配線（I2C）

| MPU-6050 | ESP32 |
| --- | --- |
| SDA | GPIO21 |
| SCL | GPIO22 |
| AD0 | GND（I2Cアドレス 0x68） |

## BLE仕様

| 項目 | 値 |
| --- | --- |
| デバイス名 | ESP32_TEST |
| Service UUID | `12345678-1234-1234-1234-1234567890ab` |
| Characteristic UUID | `abcdefab-cdef-abcd-efab-cdefabcdefab` |
| Property | NOTIFY（ESP32 → Android の一方向） |

送信データは1回12バイト。加速度3軸 + ジャイロ3軸を、各16bit符号付き整数（ビッグエンディアン）のraw値で送る。
物理量への変換はAndroid側で行う（±8g: ÷4096、±1000dps: ÷32.8）。

## セットアップ

### ESP32

1. Arduino IDEに ESP32 ボードを追加する。
2. `esp32/` 内の `.ino` を開き、ESP32に書き込む。
3. MPU-6050は Adafruitライブラリを使わず、Wireによるレジスタ直接アクセスで初期化している（`begin()` が失敗する個体への対策）。

### Android

1. Android Studioで `android/` を開く。
2. 接続先ESP32のMACアドレスを `BleService.java` 内の定数に設定する。
3. Fire Tabletに開発者モードでインストールする。

### Python（解析）

```bash
conda create -n runform python=3.11
conda activate runform
conda install -c conda-forge pandas numpy matplotlib
```

CSVは `time_ms, ax_g, ay_g, az_g, gx_dps, gy_dps, gz_dps` の7列。
合成加速度は `sqrt(ax_g^2 + ay_g^2 + az_g^2)` で算出できる。

## 開発の経緯（主な技術課題）

- **MPU-6050の初期化**: Adafruitライブラリの `begin()` が失敗するため、Wireによるレジスタ直接アクセスに切り替えた。
- **BLEの非同期処理**: `connectGatt()` は非同期のため、記録開始を `onServicesDiscovered()` のコールバック内に移し、接続確立後にのみ記録を始めるようにした。
- **サンプリングレートの改善**: 当初の実効サンプリングレートは約8.3Hzだった。BLE接続間隔の短縮要求（ESP32側 `updateConnParams` / Android側 `requestConnectionPriority`）と、ESP32のシリアル出力削減（9600→115200bps、loop内出力の削除）により、約21.7Hz（目標20Hz）まで改善した。

## 今後の予定

- 屋外走行データの収集とケイデンス検出のしきい値決定
- Gemini APIによるフィードバック実装
- リアルタイム波形グラフの表示
- 歩行解析への対応

## ライセンス

未定（個人の課題制作）。