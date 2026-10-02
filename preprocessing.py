"""Unicode-safe message normalization and lightweight entity extraction."""
from __future__ import annotations
import re
import unicodedata
from dataclasses import dataclass

URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>]+", re.I)
PHONE_RE = re.compile(r"(?<!\w)(?:\+?92[- ]?)?0?3\d{2}[- ]?\d{7}(?!\w)")
CURRENCY_RE = re.compile(r"(?:rs\.?\s?[\d,]+|\b\d[\d,]*\s?(?:pkr|rupees?)\b|₨\s?[\d,]+)", re.I)

@dataclass
class PreparedMessage:
    original: str
    normalized: str
    urls: list[str]
    phone_numbers: list[str]
    currency_amounts: list[str]

def preprocess(text: str) -> PreparedMessage:
    original = text or ""
    # NFKC folds compatibility forms while retaining Urdu script.
    normalized = unicodedata.normalize("NFKC", original).replace("\u200c", "").replace("\u200d", "")
    urls = URL_RE.findall(normalized)
    phones = PHONE_RE.findall(normalized)
    amounts = CURRENCY_RE.findall(normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip().lower()
    normalized = re.sub(r"([!?.,])\1{2,}", r"\1\1", normalized)
    return PreparedMessage(original, normalized, urls, phones, amounts)
