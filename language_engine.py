"""Small, transparent language heuristic for English, Urdu and Roman Urdu."""
import re

ROMAN_URDU = {"apko", "apka", "apni", "apna", "bhejein", "bhejo", "inaam", "mubarak", "paisa", "paise", "rupay", "jaldi", "foran", "abhi", "karein", "karo", "band", "hai", "hain", "kal", "aaj", "saath", "le", "ana", "aana", "milay", "mila", "jeet", "warna", "tasdeeq", "raqam", "aap", "ko", "se"}
ENGLISH = {"the", "your", "account", "verify", "urgent", "winner", "prize", "reward", "click", "claim", "password", "money", "today", "please", "will", "has", "been", "is", "and", "for", "to", "with", "suspended"}
URDU_RE = re.compile(r"[\u0600-\u06ff]")

def detect_language(text: str) -> str:
    if not text or not text.strip(): return "Unknown"
    words = set(re.findall(r"[a-z]+", text.lower()))
    urdu_chars = len(URDU_RE.findall(text))
    latin_chars = sum(c.isascii() and c.isalpha() for c in text)
    roman_hits, english_hits = len(words & ROMAN_URDU), len(words & ENGLISH)
    has_roman = roman_hits >= 2 or (roman_hits >= 1 and len(words) < 8)
    has_english = english_hits >= 2
    if urdu_chars and (latin_chars or has_english or has_roman): return "Mixed / Urdu"
    if urdu_chars: return "Urdu"
    if has_roman and has_english: return "Mixed / Roman Urdu"
    if has_roman: return "Roman Urdu"
    return "English" if latin_chars else "Unknown"
