import streamlit as st
import time
from typing import Optional, Any, Callable
from config import Config

class ErrorHandler:
    @staticmethod
    def handle_error(error: Exception, custom_message: Optional[str] = None) -> None:
        """
        エラーをStreamlitで表示
        """
        error_msg = custom_message or Config.ERROR_MESSAGES.get(
            'processing_error', '処理中にエラーが発生しました: {}'
        ).format(str(error))
        st.error(error_msg)

    @staticmethod
    def retry_on_failure(
        func: Callable,
        max_attempts: int = Config.MAX_RETRY_ATTEMPTS,
        delay: int = Config.RETRY_DELAY,
        custom_error_msg: Optional[str] = None
    ) -> Any:
        """
        失敗時に自動リトライを行う
        """
        last_error = None

        for attempt in range(max_attempts):
            try:
                return func()
            except Exception as e:
                last_error = e
                if attempt < max_attempts - 1:
                    st.warning(f"エラーが発生しました。再試行中... ({attempt + 1}/{max_attempts})")
                    time.sleep(delay)
                else:
                    error_msg = custom_error_msg or f"最大試行回数に達しました: {str(e)}"
                    ErrorHandler.handle_error(e, error_msg)
                    raise e

        return None

    @staticmethod
    def validate_api_key() -> bool:
        """
        API キーの存在を確認
        """
        if not Config.GEMINI_API_KEY:
            st.error(Config.ERROR_MESSAGES['no_api_key'])
            return False
        return True

    @staticmethod
    def validate_file_type(file_name: str) -> bool:
        """
        ファイルタイプの検証
        """
        file_extension = file_name.lower().split('.')[-1]
        if file_extension not in Config.SUPPORTED_FILE_TYPES:
            st.error(Config.ERROR_MESSAGES['unsupported_file'])
            return False
        return True

    @staticmethod
    def show_page_error(page_num: int) -> None:
        """
        ページ読み取りエラーの表示
        """
        st.warning(Config.ERROR_MESSAGES['page_read_error'].format(page_num))