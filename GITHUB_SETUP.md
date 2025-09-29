# GitHub連携手順

## 現在の状況
ローカルで開発済みだが、まだGitリポジトリが初期化されていない状態

## セットアップ手順

### 1. ローカルでGitリポジトリを初期化

```bash
# Gitリポジトリの初期化
git init

# ユーザー情報の設定（まだの場合）
git config user.name "Your Name"
git config user.email "your.email@example.com"

# すべてのファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: PDF解析システム"
```

### 2. GitHubでリポジトリを作成

1. [GitHub](https://github.com) にログイン
2. 右上の「+」→「New repository」をクリック
3. 以下を設定：
   - **Repository name**: `demo_pdf_summary`
   - **Description**: `PDFや画像ファイルをGemini APIで解析するシステム`
   - **Public/Private**: お好みで選択
   - **Initialize this repository**: チェックしない（既存コードがあるため）
4. 「Create repository」をクリック

### 3. リモートリポジトリと連携

GitHubでリポジトリを作成後、表示されるURLをコピーして：

```bash
# リモートリポジトリを追加
git remote add origin https://github.com/YOUR_USERNAME/demo_pdf_summary.git

# ブランチ名をmainに変更（必要な場合）
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

### 4. 重要：秘密情報の確認

プッシュ前に以下のファイルが `.gitignore` に含まれているか確認：

```bash
# 確認コマンド
cat .gitignore

# 以下が含まれているはず：
# .env
# .streamlit/secrets.toml
```

⚠️ **警告**: APIキーが含まれるファイルは絶対にプッシュしないでください！

### 5. もしAPIキーを誤ってコミットしてしまった場合

```bash
# 履歴から削除
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env .streamlit/secrets.toml" \
  --prune-empty --tag-name-filter cat -- --all

# または BFG Repo-Cleaner を使用（より簡単）
# https://rtyley.github.io/bfg-repo-cleaner/
```

## 今すぐ実行する簡単な手順

```bash
# 1. Gitの初期化とコミット
git init
git add .
git commit -m "Initial commit: PDF解析システム"

# 2. GitHubでリポジトリを作成（ブラウザで）

# 3. リモート追加とプッシュ（YOUR_USERNAMEを置き換え）
git remote add origin https://github.com/YOUR_USERNAME/demo_pdf_summary.git
git branch -M main
git push -u origin main
```

## Streamlit Cloudでデプロイ

GitHubにプッシュ後：

1. [Streamlit Cloud](https://share.streamlit.io/) にアクセス
2. 「New app」→ GitHubリポジトリを選択
3. Secrets設定で `GEMINI_API_KEY` を追加
4. デプロイ！

## トラブルシューティング

### Permission deniedエラーの場合

SSHキーまたはPersonal Access Tokenの設定が必要：

#### Personal Access Token（推奨）
1. GitHub → Settings → Developer settings → Personal access tokens
2. 「Generate new token」
3. 権限を選択（repo にチェック）
4. トークンをコピー
5. プッシュ時にパスワードの代わりに使用

#### SSHキーの場合
```bash
# SSHキー生成
ssh-keygen -t ed25519 -C "your.email@example.com"

# 公開鍵をコピー
cat ~/.ssh/id_ed25519.pub

# GitHubのSettings → SSH and GPG keys → New SSH keyで追加
```

### 大きなファイルがある場合

```bash
# 100MB以上のファイルがある場合はGit LFSを使用
git lfs track "*.pdf"
git add .gitattributes
```

## 次のステップ

1. GitHubへのプッシュ完了後、READMEにバッジを追加
2. GitHub Actionsでテストを自動化
3. Streamlit Cloudでデプロイ
4. カスタムドメインの設定（オプション）