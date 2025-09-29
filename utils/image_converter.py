from PIL import Image
import io
from typing import List, Optional, Union
import streamlit as st
from pdf2image import convert_from_bytes
from config import Config

class ImageConverter:
    @staticmethod
    def pdf_to_images(pdf_bytes: bytes, dpi: int = Config.IMAGE_DPI) -> List[Image.Image]:
        """
        PDFバイトデータを画像のリストに変換
        """
        try:
            images = convert_from_bytes(pdf_bytes, dpi=dpi)
            return images
        except Exception as e:
            st.error(f"PDFの画像変換中にエラーが発生しました: {str(e)}")
            return []

    @staticmethod
    def image_to_bytes(image: Image.Image, format: str = 'PNG') -> bytes:
        """
        PIL Imageをバイトデータに変換
        """
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=format)
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr

    @staticmethod
    def resize_image_if_needed(image: Image.Image, max_width: int = 1920, max_height: int = 1080) -> Image.Image:
        """
        画像が大きすぎる場合はリサイズ
        """
        width, height = image.size

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return image

    @staticmethod
    def process_uploaded_image(uploaded_file) -> Optional[Image.Image]:
        """
        アップロードされた画像ファイルを処理
        """
        try:
            image = Image.open(uploaded_file)
            image = ImageConverter.resize_image_if_needed(image)
            return image
        except Exception as e:
            st.error(f"画像の読み込み中にエラーが発生しました: {str(e)}")
            return None

    @staticmethod
    def batch_images(images: List[Image.Image], batch_size: int = Config.MAX_PAGES_PER_BATCH) -> List[List[Image.Image]]:
        """
        画像リストをバッチに分割
        """
        batches = []
        for i in range(0, len(images), batch_size):
            batch = images[i:i + batch_size]
            batches.append(batch)
        return batches