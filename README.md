# PDF解析システム

PDFや画像ファイルをアップロードして、Google Gemini APIで内容を解析・要約するWebアプリケーションです。

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

## 🚀 Streamlit Cloudへのデプロイ

詳細な手順は[DEPLOY.md](DEPLOY.md)を参照してください。

### クイックデプロイ手順
1. このリポジトリをGitHubにプッシュ
2. [Streamlit Cloud](https://share.streamlit.io/)でアプリを作成
3. Secrets設定で`GEMINI_API_KEY`を追加
4. デプロイ完了！

## 機能

- PDFおよび画像ファイル（PNG、JPEG）のアップロード対応
- 複数ファイルの同時アップロード・解析
- 大容量ファイルの分割処理（50ページごと）
- 図面や表などの視覚情報も含めた解析
- 進捗表示付きの処理
- 日本語での解析結果出力

## クイックスタート（自動セットアップ）

### macOS/Linux
```bash
# セットアップスクリプトの実行
./setup.sh

# アプリケーションの起動
source venv/bin/activate
streamlit run app.py
```

### Windows
```batch
# セットアップスクリプトの実行
setup.bat

# アプリケーションの起動
venv\Scripts\activate.bat
streamlit run app.py
```

## 手動セットアップ

### 1. 必要な環境

- Python 3.8以上
- Poppler（PDF処理用）

### 2. 仮想環境の作成（推奨）

#### Pythonのvenvを使用する場合
```bash
# 仮想環境の作成
python3 -m venv venv

# 仮想環境の有効化（macOS/Linux）
source venv/bin/activate

# 仮想環境の有効化（Windows）
# PowerShell
venv\Scripts\Activate.ps1
# または Command Prompt
venv\Scripts\activate.bat
```

#### Anacondaを使用する場合
```bash
# 仮想環境の作成
conda create -n pdf_analyzer python=3.8

# 仮想環境の有効化
conda activate pdf_analyzer
```

### 3. Popplerのインストール

#### macOS
```bash
brew install poppler
```

#### Ubuntu/Debian
```bash
sudo apt-get install poppler-utils
```

#### Windows
1. [Popplerのダウンロードページ](http://blog.alivate.com.au/poppler-windows/)からバイナリをダウンロード
2. 解凍してPATHに追加

### 4. 依存ライブラリのインストール

```bash
# 仮想環境が有効化されていることを確認してから実行
pip install -r requirements.txt
```

### 5. Gemini API キーの設定

1. [Google AI Studio](https://makersuite.google.com/app/apikey)でAPIキーを取得
2. `.env.example`をコピーして`.env`ファイルを作成
```bash
cp .env.example .env
```
3. `.env`ファイルにAPIキーを設定
```
GEMINI_API_KEY=your_actual_api_key_here
```

## 使用方法

### アプリケーションの起動

```bash
# 仮想環境が有効化されていることを確認
# (venv) または (pdf_analyzer) が表示されているはず

streamlit run app.py
```

ブラウザが自動的に開き、`http://localhost:8501`でアプリケーションが表示されます。

### 仮想環境の無効化

作業が終了したら、以下のコマンドで仮想環境を無効化できます：

```bash
# venvの場合
deactivate

# Anacondaの場合
conda deactivate
```

### ファイルの解析

1. 「PDFまたは画像ファイルを選択してください」からファイルを選択
2. 複数ファイルを選択可能
3. 「解析開始」ボタンをクリック
4. 処理が完了すると解析結果が表示されます

## プロジェクト構成

```
demo_pdf_summary/
├── app.py                    # メインアプリケーション
├── config.py                 # 設定管理
├── requirements.txt          # 依存ライブラリ
├── .env.example             # 環境変数テンプレート
├── components/
│   ├── file_uploader.py    # ファイルアップロード処理
│   ├── pdf_processor.py    # PDF処理
│   └── gemini_analyzer.py  # Gemini API連携
└── utils/
    ├── error_handler.py     # エラー処理
    └── image_converter.py   # 画像変換ユーティリティ
```

## 解析結果の形式

解析結果は以下の構造で出力されます：

1. **要点・概要** - 文書の主要な内容と目的
2. **詳細分析（データ抽出）** - 重要な情報、データ、数値の抽出
3. **数値データ・概算** - 該当する場合の数量、金額、統計データなど
4. **補足情報・留意点** - 注意事項、制限事項、追加情報など

## トラブルシューティング

### "Gemini API キーが設定されていません"エラー
- `.env`ファイルが存在することを確認
- APIキーが正しく設定されているか確認

### PDFが読み込めない
- Popplerがインストールされているか確認
- PDFファイルが破損していないか確認

### 処理が遅い
- 大きなPDFファイルは50ページごとに分割処理されます
- 画像解像度は200 DPIに設定されています（config.pyで調整可能）

## 注意事項

- APIの使用量に応じて料金が発生する場合があります
- 大容量ファイルの処理には時間がかかることがあります
- セッション終了時に解析結果は失われます（履歴保存機能なし）# Force redeploy 2025年 9月29日 月曜日 22時28分02秒 JST
