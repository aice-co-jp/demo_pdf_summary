#!/usr/bin/env python3
"""
Gemini API接続テストスクリプト
APIキーが正しく設定されているか確認します
"""

import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# .envファイルを読み込み
load_dotenv()

def test_api_connection():
    """APIキーをテストする"""
    print("=" * 50)
    print("Gemini API 接続テスト")
    print("=" * 50)

    # APIキーの確認
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        print("❌ エラー: APIキーが見つかりません")
        print("   .envファイルにGEMINI_API_KEYを設定してください")
        return False

    print(f"✓ APIキーを検出しました")
    print(f"  キーの最初の10文字: {api_key[:10]}...")
    print(f"  キーの長さ: {len(api_key)}文字")

    # APIの設定
    try:
        print("\nAPIを設定中...")
        genai.configure(api_key=api_key)
        print("✓ API設定完了")
    except Exception as e:
        print(f"❌ API設定エラー: {e}")
        return False

    # モデルの初期化テスト
    try:
        print("\nモデルを初期化中...")
        model = genai.GenerativeModel('gemini-1.5-pro')
        print("✓ モデル初期化完了")
    except Exception as e:
        print(f"❌ モデル初期化エラー: {e}")
        return False

    # 簡単なテキスト生成テスト
    try:
        print("\nテキスト生成テスト中...")
        response = model.generate_content("Hello, please respond with 'OK' if you receive this.")
        print(f"✓ テスト成功！")
        print(f"  レスポンス: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ テキスト生成エラー: {e}")
        print("\n考えられる原因:")
        print("1. APIキーが無効または期限切れ")
        print("2. APIの利用制限に達している")
        print("3. ネットワーク接続の問題")
        print("4. Gemini APIサービスの一時的な問題")
        return False

    print("\n" + "=" * 50)
    print("✅ すべてのテストが成功しました！")
    print("APIは正常に動作しています。")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = test_api_connection()
    sys.exit(0 if success else 1)