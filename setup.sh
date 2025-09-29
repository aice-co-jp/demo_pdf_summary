#!/bin/bash

echo "=========================================="
echo "PDF解析システム セットアップスクリプト"
echo "=========================================="
echo ""

# OSの検出
OS_TYPE=""
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="mac"
    echo "✓ macOSを検出しました"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
    echo "✓ Linuxを検出しました"
else
    echo "⚠️  サポートされていないOSです。手動でセットアップしてください。"
    exit 1
fi

# Pythonのバージョン確認
echo ""
echo "1. Pythonバージョンの確認..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3がインストールされていません"
    echo "   Python 3.8以上をインストールしてください"
    exit 1
fi

# 仮想環境の作成
echo ""
echo "2. 仮想環境の作成..."
if [ -d "venv" ]; then
    echo "   既存の仮想環境が見つかりました。スキップします。"
else
    python3 -m venv venv
    echo "✓ 仮想環境を作成しました"
fi

# 仮想環境の有効化
echo ""
echo "3. 仮想環境の有効化..."
source venv/bin/activate
echo "✓ 仮想環境を有効化しました"

# Popplerのインストール確認
echo ""
echo "4. Popplerのインストール確認..."
if command -v pdfinfo &> /dev/null; then
    echo "✓ Popplerは既にインストールされています"
else
    echo "⚠️  Popplerがインストールされていません"
    if [ "$OS_TYPE" == "mac" ]; then
        echo "   Homebrewでインストールしますか？ (y/n)"
        read -r response
        if [[ "$response" == "y" ]]; then
            brew install poppler
        else
            echo "   手動でインストールしてください: brew install poppler"
        fi
    elif [ "$OS_TYPE" == "linux" ]; then
        echo "   以下のコマンドでインストールしてください："
        echo "   sudo apt-get install poppler-utils"
    fi
fi

# 依存ライブラリのインストール
echo ""
echo "5. 依存ライブラリのインストール..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ 依存ライブラリをインストールしました"

# .envファイルの作成
echo ""
echo "6. 環境変数ファイルの設定..."
if [ -f ".env" ]; then
    echo "   .envファイルは既に存在します"
else
    cp .env.example .env
    echo "✓ .envファイルを作成しました"
    echo ""
    echo "⚠️  重要: .envファイルにGemini APIキーを設定してください"
    echo "   1. https://makersuite.google.com/app/apikey でAPIキーを取得"
    echo "   2. .envファイルを編集してAPIキーを設定"
fi

echo ""
echo "=========================================="
echo "セットアップが完了しました！"
echo ""
echo "アプリケーションを起動するには："
echo "  source venv/bin/activate  # 仮想環境を有効化"
echo "  streamlit run app.py       # アプリを起動"
echo ""
echo "仮想環境を終了するには："
echo "  deactivate"
echo "=========================================="