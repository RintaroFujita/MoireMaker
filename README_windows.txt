# Moire Pattern Generator for Windows

## 必要なもの
- Windows 10/11
- Python 3.8以降（exe化する場合は不要）

## 1. 依存パッケージのインストール

コマンドプロンプトで以下を実行してください：

```
pip install -r requirements.txt
```

GPU機能を使いたい場合は
```
pip install pyopencl numba
```
も追加で実行してください。

## 2. 実行方法

```
python pyqt_moire.py
```

## 3. exeファイル化（スタンドアロン化）

1. PyInstallerをインストール
```
pip install pyinstaller
```
2. exe化コマンドを実行
```
pyinstaller --onefile --windowed pyqt_moire.py
```
3. `dist/pyqt_moire.exe` が生成されます。

## 4. 注意事項
- GPU機能はPCの環境・ドライバによって動作しない場合があります。
- exe化後はPythonがインストールされていないPCでも動作します。
- 実行時にウイルス対策ソフトが警告を出す場合がありますが、問題ありません。

## 5. サポート
ご不明点は開発者までご連絡ください。 