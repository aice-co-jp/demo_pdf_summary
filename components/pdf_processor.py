import streamlit as st
from typing import List, Dict, Any, Optional
from PIL import Image
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.image_converter import ImageConverter
from utils.error_handler import ErrorHandler
from config import Config

class PDFProcessor:
    def __init__(self):
        self.image_converter = ImageConverter()
        self.error_handler = ErrorHandler()

    def process_pdf(self, uploaded_file) -> List[Image.Image]:
        """
        PDFファイルを処理して画像リストを返す
        """
        try:
            pdf_bytes = uploaded_file.read()

            images = self.image_converter.pdf_to_images(pdf_bytes)

            if not images:
                st.error(Config.ERROR_MESSAGES['file_corrupted'])
                return []

            return images

        except Exception as e:
            self.error_handler.handle_error(e, "PDFの処理中にエラーが発生しました")
            return []

    def process_image(self, uploaded_file) -> Optional[Image.Image]:
        """
        画像ファイルを処理
        """
        return self.image_converter.process_uploaded_image(uploaded_file)

    def process_multiple_files(self, uploaded_files) -> Dict[str, List[Image.Image]]:
        """
        複数のファイルを処理
        """
        all_files_data = {}

        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            file_extension = file_name.lower().split('.')[-1]

            if not self.error_handler.validate_file_type(file_name):
                continue

            st.info(f"処理中: {file_name}")

            if file_extension == 'pdf':
                images = self.process_pdf(uploaded_file)
                if images:
                    all_files_data[file_name] = images
            else:
                image = self.process_image(uploaded_file)
                if image:
                    all_files_data[file_name] = [image]

        return all_files_data

    def prepare_batches(self, files_data: Dict[str, List[Image.Image]]) -> List[Dict[str, Any]]:
        """
        ファイルデータをバッチに分割
        """
        all_batches = []

        for file_name, images in files_data.items():
            if len(images) > Config.MAX_PAGES_PER_BATCH:
                batched_images = self.image_converter.batch_images(images)
                for batch_idx, batch in enumerate(batched_images):
                    all_batches.append({
                        'file_name': file_name,
                        'batch_number': batch_idx + 1,
                        'total_batches': len(batched_images),
                        'images': batch
                    })
            else:
                all_batches.append({
                    'file_name': file_name,
                    'batch_number': 1,
                    'total_batches': 1,
                    'images': images
                })

        return all_batches