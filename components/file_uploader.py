import streamlit as st
from typing import List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

class FileUploader:
    def __init__(self):
        self.supported_types = Config.SUPPORTED_FILE_TYPES

    def create_upload_widget(self) -> Optional[List]:
        """
        ファイルアップロードウィジェットを作成
        """
        uploaded_files = st.file_uploader(
            Config.UPLOAD_HELP,
            type=self.supported_types,
            accept_multiple_files=True,
            key="file_uploader"
        )

        return uploaded_files if uploaded_files else None

    def display_uploaded_files_info(self, uploaded_files: List) -> None:
        """
        アップロードされたファイルの情報を表示
        """
        if not uploaded_files:
            return

        st.success(Config.SUCCESS_MESSAGES['upload_complete'])

        with st.expander("アップロードされたファイル一覧"):
            for file in uploaded_files:
                file_size = len(file.read()) / 1024 / 1024
                file.seek(0)
                st.write(f"- {file.name} ({file_size:.2f} MB)")

    def validate_files(self, uploaded_files: List) -> bool:
        """
        アップロードされたファイルを検証
        """
        if not uploaded_files:
            st.warning("ファイルをアップロードしてください。")
            return False

        for file in uploaded_files:
            file_extension = file.name.lower().split('.')[-1]
            if file_extension not in self.supported_types:
                st.error(f"{file.name}: {Config.ERROR_MESSAGES['unsupported_file']}")
                return False

        return True