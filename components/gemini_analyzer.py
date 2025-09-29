import google.generativeai as genai
import streamlit as st
from typing import List, Dict, Any
from PIL import Image
import time
import sys
import os
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.error_handler import ErrorHandler
from utils.image_converter import ImageConverter
from config import Config

class GeminiAnalyzer:
    def __init__(self):
        self.error_handler = ErrorHandler()
        self.image_converter = ImageConverter()
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """
        Gemini APIの初期化
        """
        if not self.error_handler.validate_api_key():
            st.error("APIキーが設定されていません。.envファイルを確認してください。")
            return

        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            # 初期化成功のログは表示しない（UIをクリーンに保つため）
            pass
        except Exception as e:
            st.error(f"Gemini APIの初期化に失敗しました: {str(e)}")
            st.error(f"APIキーの最初の10文字: {Config.GEMINI_API_KEY[:10] if Config.GEMINI_API_KEY else 'なし'}...")
            self.error_handler.handle_error(e, "Gemini APIの初期化に失敗しました")

    def analyze_images(self, images: List[Image.Image], prompt: str = Config.ANALYSIS_PROMPT) -> str:
        """
        画像リストを解析して結果を返す
        """
        if not self.model:
            return "モデルが初期化されていません。API キーを確認してください。"

        try:
            def _analyze():
                # 画像数を確認（デバッグ時のみ表示）
                # st.info(f"📄 {len(images)}ページの画像を解析中...")

                # 画像サイズを確認して必要に応じてリサイズ
                processed_images = []
                for i, img in enumerate(images):
                    # 大きすぎる画像はリサイズ
                    resized_img = self.image_converter.resize_image_if_needed(img)
                    processed_images.append(resized_img)

                # Gemini APIへ送信
                response = self.model.generate_content([prompt] + processed_images)

                # レスポンスの確認
                if response and hasattr(response, 'text'):
                    return response.text
                else:
                    st.error("APIレスポンスにテキストが含まれていません")
                    return None

            result = self.error_handler.retry_on_failure(
                _analyze,
                custom_error_msg="Gemini APIの呼び出しに失敗しました"
            )

            return result if result else "解析結果を取得できませんでした。"

        except Exception as e:
            # 詳細なエラー情報を表示
            st.error(f"画像解析エラー: {str(e)}")
            st.error(f"エラータイプ: {type(e).__name__}")
            st.text("スタックトレース:")
            st.code(traceback.format_exc())
            return "解析に失敗しました。"

    def analyze_batch(self, batch_data: Dict[str, Any], progress_bar=None) -> str:
        """
        バッチデータを解析
        """
        file_name = batch_data['file_name']
        batch_number = batch_data['batch_number']
        total_batches = batch_data['total_batches']
        images = batch_data['images']

        if total_batches > 1:
            st.info(f"処理中: {file_name} - バッチ {batch_number}/{total_batches}")

        result = self.analyze_images(images)

        if progress_bar:
            progress_bar.progress(batch_number / total_batches)

        return result

    def combine_batch_results(self, results: List[str], file_name: str) -> str:
        """
        複数のバッチ結果を統合
        """
        if len(results) == 1:
            return results[0]

        combined = f"## ファイル: {file_name}\n\n"
        combined += "### 統合解析結果\n\n"

        for i, result in enumerate(results, 1):
            if len(results) > 1:
                combined += f"#### セクション {i}\n"
            combined += result + "\n\n"

        return combined

    def analyze_all_batches(self, all_batches: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        すべてのバッチを解析して結果を返す
        """
        results_by_file = {}
        total_batches = len(all_batches)

        progress_bar = st.progress(0)
        progress_text = st.empty()

        for idx, batch_data in enumerate(all_batches):
            file_name = batch_data['file_name']

            progress_text.text(
                Config.SUCCESS_MESSAGES['page_progress'].format(idx + 1, total_batches)
            )

            result = self.analyze_batch(batch_data)

            if file_name not in results_by_file:
                results_by_file[file_name] = []
            results_by_file[file_name].append(result)

            progress_bar.progress((idx + 1) / total_batches)
            time.sleep(0.1)

        progress_bar.empty()
        progress_text.empty()

        final_results = {}
        for file_name, batch_results in results_by_file.items():
            final_results[file_name] = self.combine_batch_results(batch_results, file_name)

        return final_results