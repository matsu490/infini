# Change Log

## [v0.1.3](https://github.com/matsu490/infini/tree/v0.1.3) (2018-04-11)
**Implemented enhancements:**
- ログファイルをエクセルで開いている時に生じる、書き込み不可エラーへの対処をした（チケット #2464 参照）
- マッチングの際、judge_table に False が含まれていても OK 判定を返すバグの修正をした（チケット #2464 参照）

## [v0.1.2](https://github.com/matsu490/infini/tree/v0.1.2) (2018-01-17)
**Implemented enhancements:**
- typo (Envinfo -> EnvInfo)
- 内部環境情報のカラムラベルの順序を変更した（チケット #2458 参照）
- ANALOG_SENSOR_PERIOD を一時的に追加した（アナログセンサーグループの実装とともに消す予定）

## [v0.1.1](https://github.com/matsu490/infini/tree/v0.1.1) (2018-01-16)
**Implemented enhancements:**
- タイムスタンプの月、日を 0 埋めして二桁表示にした

## [v0.1.0](https://github.com/matsu490/infini/tree/v0.1.0) (2017-12-27)
**Implemented enhancements:**
- 初めてのリリース
- デバイス多台数検証用スクリプト
- データマッチングスクリプト

## ToDo
- [ ] データマッチングスクリプト、読み込みデータの不具合による例外処理を追加する
- [x] アナログセンサーグループの実装
