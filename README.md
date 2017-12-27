# infini
====

# Description
デバイス多台数検証用スクリプトとデータマッチングスクリプト

# Contents
- デバイス多台数検証用スクリプト（main2.py, params.py）
- データマッチングスクリプト（matching.py）

# Usage
## デバイス多台数検証用スクリプト
指定台数の仮想デバイスを起動し、MQTT を使用してサーバーにデータを送信します。

### 設定
`params.py` で行います。

- `USERNAME`: MQTT クライアントのユーザーネーム
- `PASSWORD`: MQTT クライアントのパスワード
- `HOST`: MQTT ブローカーの ホスト名または IP アドレス

- `N_DEVICE`: 起動する仮想デバイスの数

- `BEACON_PERIOD`: ビーコンデータを送出する間隔（秒）
- `ENV_PERIOD`:  内部環境情報を送出する間隔（秒）
- `DIGITAL_SENSOR_PERIOD`: デジタルセンサーデータを送出する間隔（秒）
- `DIGITAL_COUNTER_PERIODS`: デジタルカウンターデータを送出する間隔（秒）

### 起動
`$ python main2.py`

## データマッチングスクリプト
サーバーからダウンロードしたセンサーデータ（以下、サーバーデータ）と、仮想デバイスからデータ送出時にローカルに保存したセンサーデータ（以下、ローカルデータ）のマッチングを行います。

### 設定
`matching.py` 内で行います。

- `device_id`: 何番のデバイスのデータをマッチングするかを指定
- `sensor_names`: マッチングの対象とするセンサーの名前、内部環境情報（`Envinfo`）、アナログセンサー（`Analog_sensors`）、デジタルセンサー（`Digital_sensors`）、デジタルカウンター（`Digital_counters`）、ビーコン（`Beacon`）
- `time_stamp`: マッチングを行うローカルデータのタイムスタンプ
- `begin`: この時刻からのデータをマッチングの対象とする
- `end`: この時刻までのデータをマッチングの対象とする

### 起動
`$ python matching.py`

### 出力
センサー名に対してマッチングの結果（データに不一致や欠落がなければ `OK`、あれば `NG`）が出力される

# Install
以下のコマンドで任意のディレクトリに clone してください。  
`$ git clone git@github.com:matsu490/infini.git`  
または任意のディレクトリに ZIP ファイルをダウンロードして解凍してください。

# Requirement
- Python 2.7.x
- Pandas

# Author
[matsu490](https://github.com/matsu490)
