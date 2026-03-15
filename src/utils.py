"""Utility functions for CV AI agent."""
from pathlib import Path
from typing import Dict, List

from .cv_parser import extract_text_from_pdf
from .feature_extraction import parse_cv


def load_and_parse_cvs(file_paths: List[str]) -> List[Dict]:
    """Load multiple CV PDF files and parse features."""
    result = []
    for path in file_paths:
        text = extract_text_from_pdf(path)
        features = parse_cv(text)
        features.update({"file": path})
        result.append(features)
    return result


def safe_text(value) -> str:
    if value is None:
        return ""
    return str(value)
