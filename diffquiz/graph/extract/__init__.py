"""Extractor registry — map a file path to the right language extractor."""
from __future__ import annotations

from .base import LanguageExtractor
from .python import PythonExtractor

EXTRACTORS: list[LanguageExtractor] = [PythonExtractor()]


def for_path(path: str) -> LanguageExtractor | None:
    for extractor in EXTRACTORS:
        if path.endswith(extractor.extensions):
            return extractor
    return None
