@echo off
echo ==========================================
echo PDF解析システム セットアップスクリプト
echo ==========================================
echo.

REM Pythonのバージョン確認
echo 1. Pythonバージョンの確認...
python --version 2>NUL
if %errorlevel% neq 0 (
    echo × Python3がインストールされていません
    echo   Python 3.8以上をインストールしてください
    pause
    exit /b 1
)
echo √ Pythonが検出されました

REM 仮想環境の作成
echo.
echo 2. 仮想環境の作成...
if exist venv (
    echo   既存の仮想環境が見つかりました。スキップします。
) else (
    python -m venv venv
    echo √ 仮想環境を作成しました
)

REM 仮想環境の有効化
echo.
echo 3. 仮想環境の有効化...
call venv\Scripts\activate.bat
echo √ 仮想環境を有効化しました

REM 依存ライブラリのインストール
echo.
echo 5. 依存ライブラリのインストール...
pip install --upgrade pip
pip install -r requirements.txt
echo √ 依存ライブラリをインストールしました

REM .envファイルの作成
echo.
echo 6. 環境変数ファイルの設定...
if exist .env (
    echo   .envファイルは既に存在します
) else (
    copy .env.example .env
    echo √ .envファイルを作成しました
    echo.
    echo ※重要: .envファイルにGemini APIキーを設定してください
    echo   1. https://makersuite.google.com/app/apikey でAPIキーを取得
    echo   2. .envファイルを編集してAPIキーを設定
)

echo.
echo ==========================================
echo セットアップが完了しました！
echo.
echo ※注意: Popplerを手動でインストールする必要があります
echo   1. http://blog.alivate.com.au/poppler-windows/ からダウンロード
echo   2. 解凍してPATHに追加
echo.
echo アプリケーションを起動するには：
echo   venv\Scripts\activate.bat  # 仮想環境を有効化
echo   streamlit run app.py        # アプリを起動
echo.
echo 仮想環境を終了するには：
echo   deactivate
echo ==========================================
pause