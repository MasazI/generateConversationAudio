# 会話音声の生成

このリポジトリは、Amazon Pollyを使用して会話音声ファイルを生成するためのコードです。

[English README](README.md)

### 前提条件
- Python 3.XX
- boto3 SDK
- ffmpeg

実行する前に、AWS認証情報を環境変数に設定する必要があります。

### 台本ファイルの準備
```
cp conversation-sample.csv conversation.csv
```

### 音声ファイルの生成
```
python generateScriptCsv.py
```