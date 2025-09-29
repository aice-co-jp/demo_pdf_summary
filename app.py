import streamlit as st
from config import Config
from components.file_uploader import FileUploader
from components.pdf_processor import PDFProcessor
from components.gemini_analyzer import GeminiAnalyzer
from utils.error_handler import ErrorHandler

def main():
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # シンプルなカスタムスタイル
    st.markdown("""
    <style>
    /* メインタイトルのスタイリング */
    h1 {
        color: #2E4057;
        padding-bottom: 10px;
        border-bottom: 2px solid #FF6B6B;
    }

    /* ボタンのカスタマイズ */
    .stButton > button {
        background-color: #FF6B6B;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        background-color: #FF5252;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }

    /* ファイルアップローダーのスタイル */
    .stFileUploader {
        border: 2px dashed #FF6B6B;
        border-radius: 10px;
        padding: 20px;
    }

    /* プログレスバー */
    .stProgress > div > div {
        background-color: #FF6B6B;
    }

    /* エクスパンダーのヘッダー */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }

    /* メトリクスカード風 */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

    # ヘッダー部分
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("📄 " + Config.APP_TITLE)
        st.markdown(
            f"<p style='text-align: center; color: #6c757d; font-size: 1.1rem;'>{Config.APP_DESCRIPTION}</p>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # セッションステートの初期化
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'file_count' not in st.session_state:
        st.session_state.file_count = 0

    # メインコンテンツ
    with st.container():
        # ファイルアップロードセクション
        st.markdown("### 📁 ファイルアップロード")

        file_uploader = FileUploader()
        uploaded_files = file_uploader.create_upload_widget()

        if uploaded_files:
            st.session_state.file_count = len(uploaded_files)

            # ファイル情報を表示（メトリクス形式）
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="📎 アップロードファイル数", value=f"{len(uploaded_files)} 件")
            with col2:
                total_size = sum(len(file.read()) for file in uploaded_files) / (1024 * 1024)
                for file in uploaded_files:
                    file.seek(0)  # ファイルポインタをリセット
                st.metric(label="💾 合計サイズ", value=f"{total_size:.2f} MB")
            with col3:
                file_types = set(file.name.split('.')[-1].upper() for file in uploaded_files)
                st.metric(label="📋 ファイル形式", value=", ".join(file_types))

            # ファイルリスト
            with st.expander("📂 アップロードされたファイル詳細", expanded=False):
                for i, file in enumerate(uploaded_files, 1):
                    file_size = len(file.read()) / 1024 / 1024
                    file.seek(0)
                    st.write(f"{i}. **{file.name}** ({file_size:.2f} MB)")

            st.markdown("---")

            # 解析ボタン（中央配置）
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("🚀 解析開始", type="primary", use_container_width=True):
                    if file_uploader.validate_files(uploaded_files):
                        with st.spinner('🔄 処理中... しばらくお待ちください'):
                            st.session_state.analysis_results = process_files(uploaded_files)
        else:
            # ファイルがアップロードされていない時の案内
            st.info("👆 上のエリアにPDFまたは画像ファイルをドラッグ&ドロップ、またはクリックして選択してください")

    # 結果表示セクション
    if st.session_state.analysis_results:
        display_results(st.session_state.analysis_results)

    # フッター
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #6c757d; font-size: 0.9rem;'>Powered by Google Gemini AI | © 2024</p>",
        unsafe_allow_html=True
    )

def process_files(uploaded_files):
    """
    ファイルを処理して解析結果を返す
    """
    error_handler = ErrorHandler()

    if not error_handler.validate_api_key():
        return None

    # プログレスバーの表示
    progress_text = st.empty()
    progress_bar = st.progress(0)

    progress_text.text("📝 ファイルを準備中...")
    progress_bar.progress(0.2)

    pdf_processor = PDFProcessor()
    files_data = pdf_processor.process_multiple_files(uploaded_files)

    if not files_data:
        st.error("❌ 処理可能なファイルがありません。")
        progress_text.empty()
        progress_bar.empty()
        return None

    progress_text.text("🔄 データを処理中...")
    progress_bar.progress(0.5)

    all_batches = pdf_processor.prepare_batches(files_data)

    progress_text.text("🤖 AIで解析中...")
    progress_bar.progress(0.7)

    gemini_analyzer = GeminiAnalyzer()
    results = gemini_analyzer.analyze_all_batches(all_batches)

    progress_text.text("✅ 処理完了！")
    progress_bar.progress(1.0)

    # プログレス表示をクリア
    import time
    time.sleep(1)
    progress_text.empty()
    progress_bar.empty()

    st.success("✨ 解析が正常に完了しました！")

    return results

def display_results(results):
    """
    解析結果を表示
    """
    st.markdown("### 📊 解析結果")

    # 結果のサマリー
    st.info(f"📋 {len(results)} 件のファイルを解析しました")

    # タブ形式で結果を表示
    if len(results) > 1:
        tabs = st.tabs([f"📄 {name}" for name in results.keys()])
        for tab, (file_name, content) in zip(tabs, results.items()):
            with tab:
                st.markdown(content)
    else:
        # 1ファイルの場合はそのまま表示
        file_name, content = list(results.items())[0]
        with st.container():
            st.markdown(f"#### 📄 {file_name}")
            st.markdown(content)

    # アクションボタン
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔄 新規解析", use_container_width=True):
            st.session_state.analysis_results = None
            st.rerun()

if __name__ == "__main__":
    main()