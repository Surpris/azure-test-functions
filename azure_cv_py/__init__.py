"""
azure_cv_py.py
"""

from .utils import set_key, set_endpoint
from .constants import AZURE_COMPUTER_VISION_VERSION
from .ocr import (
    extract_characters_with_azure_cv_ocr,
    extract_full_text,
    extract_and_save_full_text_with_azure_cv_ocr
)
