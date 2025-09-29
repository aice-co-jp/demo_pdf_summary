#!/bin/bash

echo "=========================================="
echo "Streamlit Secrets セットアップ"
echo "=========================================="
echo ""

# .envファイルの存在確認
if [ -f ".env" ]; then
    echo "✓ .envファイルを検出しました"

    # .envからAPIキーを読み込む
    source .env

    if [ -n "$GEMINI_API_KEY" ]; then
        echo "✓ GEMINI_API_KEYを検出しました"

        # .streamlitディレクトリの作成
        mkdir -p .streamlit

        # secrets.tomlの作成
        cat > .streamlit/secrets.toml << EOF
# Streamlit Secrets設定
# 自動生成されたファイル - $(date)

GEMINI_API_KEY = "$GEMINI_API_KEY"
EOF

        echo "✓ .streamlit/secrets.tomlを作成しました"
        echo ""
        echo "セットアップが完了しました！"
        echo "streamlit run app.py で実行できます"
    else
        echo "❌ .envファイルにGEMINI_API_KEYが設定されていません"
        echo "   .envファイルを編集してAPIキーを設定してください"
        exit 1
    fi
else
    echo "❌ .envファイルが見つかりません"
    echo ""
    echo "手動でセットアップする場合:"
    echo "1. .streamlit/secrets.tomlを作成"
    echo "2. 以下の内容を追加:"
    echo '   GEMINI_API_KEY = "your-api-key-here"'
    exit 1
fi