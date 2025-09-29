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
以下の画像/文書（建築図面・設計図書等）を分析し、以下の5つの項目で日本語でまとめてください。

## 解析結果

### 1) 図面から読み取れた要点（根拠）
- 建物の用途、規模、構造形式
- 主要な寸法、面積、階数
- 設計コンセプトや特徴
- 図面に明記されている具体的な情報とその根拠

### 2) 数量拾い（一次概算：レンジ表示）
- 主要部材の数量（柱、梁、壁、床等）
- 各階の床面積、延床面積
- 主要な仕上げ材の数量
- 数量は概算値としてレンジ（例：100〜120㎡）で表示

### 3) 概算工事費（税別）レンジ
- 建築工事費の概算（下限〜上限）
- 設備工事費の概算（下限〜上限）
- 外構工事費の概算（下限〜上限）
- 総工事費の概算レンジ
- 坪単価または㎡単価での表示も併記

### 4) 確認できた付帯物と留意点
- 確認できた設備機器、特殊設備
- 外構、植栽、駐車場等の付帯工事
- 施工上の留意点、特殊な仕様
- リスク要因や不確定要素

### 5) 追加で精緻化すると±5%程度まで寄せられる入力
- 現時点で不足している図面や情報
- 詳細な仕様書や材料リスト
- 地盤調査データ、構造計算書
- 設備図、詳細図など、精度向上に必要な追加資料

注意：
- 数値は可能な限り具体的に、ただし概算であることを明示
- 不明な項目は「図面から確認できず」と明記
- 建築専門用語を適切に使用すること
"""