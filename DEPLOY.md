# Streamlit Cloudへのデプロイ手順

## 前提条件
- GitHubアカウントを持っている
- プロジェクトがGitHubリポジトリにプッシュされている
- Streamlit Cloudアカウントを持っている（GitHubでサインイン可能）

## デプロイ手順

### 1. GitHubへのプッシュ

```bash
# Gitリポジトリの初期化（まだの場合）
git init
git add .
git commit -m "Initial commit"

# GitHubにリポジトリを作成後
git remote add origin https://github.com/YOUR_USERNAME/demo_pdf_summary.git
git branch -M main
git push -u origin main
```

### 2. Streamlit Cloudへのデプロイ

1. [Streamlit Cloud](https://share.streamlit.io/)にアクセス
2. GitHubアカウントでサインイン
3. 「New app」をクリック
4. 以下の設定を入力：
   - **Repository**: `YOUR_USERNAME/demo_pdf_summary`
   - **Branch**: `main`
   - **Main file path**: `app.py`

### 3. シークレットの設定（重要！）

1. デプロイ画面の「Advanced settings」をクリック
2. 「Secrets」セクションに以下を入力：

```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

または、デプロイ後：
1. アプリの管理画面から「⋮」メニューをクリック
2. 「Settings」→「Secrets」を選択
3. 上記の内容を貼り付けて保存

### 4. デプロイの確認

- デプロイには数分かかります
- ログを確認して、エラーがないか確認
- デプロイ完了後、URLが発行されます

## ファイル構成（必須）

デプロイに必要なファイル：

```
demo_pdf_summary/
├── app.py                 # メインアプリ（必須）
├── requirements.txt       # Python依存関係（必須）
├── packages.txt          # システム依存関係（Poppler用、必須）
├── config.py             # 設定ファイル
├── components/           # コンポーネント
├── utils/                # ユーティリティ
└── .streamlit/
    └── config.toml       # UI設定（オプション）
```

## トラブルシューティング

### よくあるエラーと対処法

#### 1. ModuleNotFoundError
**原因**: requirements.txtに不足がある
**対処**: すべての依存ライブラリをrequirements.txtに追加

#### 2. APIキーエラー
**原因**: Secretsが設定されていない
**対処**: Settings > Secretsから GEMINI_API_KEY を設定

#### 3. Popplerエラー
**原因**: packages.txtがない
**対処**: packages.txtに`poppler-utils`を記載

#### 4. メモリエラー
**原因**: ファイルサイズが大きすぎる
**対処**:
- MAX_PAGES_PER_BATCHを減らす
- IMAGE_DPIを下げる（150に変更）

## アプリのURL

デプロイ成功後のURL形式：
```
https://YOUR-APP-NAME.streamlit.app/
```

## 更新方法

GitHubにプッシュすると自動的に再デプロイされます：

```bash
git add .
git commit -m "Update features"
git push origin main
```

## リソース制限

Streamlit Cloud（無料プラン）の制限：
- RAM: 1GB
- ストレージ: 限定的
- 同時接続数: 制限あり

大規模な使用の場合は、有料プランを検討してください。