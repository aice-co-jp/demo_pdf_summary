import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Streamlit CloudではSecretsから、ローカルでは.envから取得
    try:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    except:
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    GEMINI_MODEL = "gemini-2.5-pro-preview-03-25"

    MAX_PAGES_PER_BATCH = 50

    IMAGE_DPI = 200

    MAX_RETRY_ATTEMPTS = 3

    RETRY_DELAY = 2

    SUPPORTED_FILE_TYPES = ['pdf', 'png', 'jpg', 'jpeg']

    APP_TITLE = "PDF解析システム"
    APP_DESCRIPTION = "PDFや画像ファイルをアップロードして、AIで内容を解析・要約します"

    UPLOAD_HELP = "PDFまたは画像ファイルを選択してください（複数選択可）"

    ERROR_MESSAGES = {
        'file_corrupted': 'ファイルが破損しています。別のファイルをアップロードしてください。',
        'page_read_error': '{}ページ目が読み取れませんでした。他のページで処理を続行します。',
        'api_error': 'API エラーが発生しました。しばらく待ってから再試行してください。',
        'no_api_key': 'Gemini API キーが設定されていません。.env ファイルを確認してください。',
        'unsupported_file': 'サポートされていないファイル形式です。',
        'processing_error': '処理中にエラーが発生しました: {}',
    }

    SUCCESS_MESSAGES = {
        'upload_complete': 'ファイルのアップロードが完了しました。',
        'processing_start': '解析処理を開始します...',
        'processing_complete': '解析が完了しました。',
        'page_progress': '処理中... ({}/{}ページ完了)',
    }

    ANALYSIS_PROMPT = """
以下の画像/文書を分析し、以下の構造で日本語でまとめてください。

## 解析結果

### 1) 要点・概要
- 文書の主要な内容と目的を簡潔に説明

### 2) 詳細分析（データ抽出）
- 重要な情報、データ、数値などを抽出
- 表やグラフがある場合はその内容を整理

### 3) 数値データ・概算（該当する場合）
- 数量、金額、統計データなど
- 建築図面の場合は面積、数量拾い、概算費用など
- 該当しない場合はこのセクションは省略

### 4) 補足情報・留意点
- 注意事項、制限事項、追加で必要な情報など

注意：
- 建築図面の場合は「数量拾い」「概算」という用語を使用
- 一般文書の場合は「詳細分析」「データ抽出」という用語を使用
- 内容に応じて適切な専門用語を使用すること
"""