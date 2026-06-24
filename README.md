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

### Python（解析）

```bash
conda create -n runform python=3.11
conda activate runform
conda install -c conda-forge pandas numpy matplotlib
```

CSVは `time_ms, ax_g, ay_g, az_g, gx_dps, gy_dps, gz_dps` の7列。
合成加速度は `sqrt(ax_g^2 + ay_g^2 + az_g^2)` で算出できる。
