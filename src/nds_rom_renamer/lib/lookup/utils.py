import re
import time
from pathlib import Path

from ..common.regions import REGION_CODE_MAP


LANGUAGE_CODES = {
    "EN", "FR", "DE", "ES", "IT", "JA", "KO", "ZH", "NL", "PT",
    "RU", "PL", "CS", "DA", "FI", "SV", "NO", "TR", "EL", "HE",
    "AR", "ID", "MS", "TH", "VI", "HU", "RO", "SK", "SL", "CA",
    "ET", "LV", "LT", "HR", "SR", "UK", "BG", "FA", "HI", "BN",
    "FIL"
}

SMALL_WORDS = {
    "a", "an", "and", "as", "at", "but", "by", "for", "if", "in",
    "nor", "of", "on", "or", "per", "so", "the", "to", "vs", "via", "yet"
}

ROMAN_NUMERAL_PATTERN = re.compile(r"^[IVXLCDM]+$")

DISC_PATTERN = re.compile(r"\(Disc\s+(\d+)\)", re.IGNORECASE)
PAREN_PATTERN = re.compile(r"\(([^)]+)\)")

def is_cache_stale(path: Path, max_age: int) -> bool:
    if not path.exists():
        return True
    age = time.time() - path.stat().st_mtime
    return age > max_age


def is_language_tag(tag: str) -> bool:
    parts = [p.strip() for p in tag.split(",")]
    return bool(parts) and all(p in LANGUAGE_CODES for p in parts)


def smart_title_case(text: str) -> str:
    words = text.split(" ")
    result = []
    for i, word in enumerate(words):
        if not word:
            result.append(word)
            continue

        core = re.sub(r"[^\w]", "", word)

        if ROMAN_NUMERAL_PATTERN.match(core) and len(core) > 0:
            result.append(word)
            continue

        if core.isdigit():
            result.append(word)
            continue

        lower_word = word.lower()
        if i != 0 and i != len(words) - 1 and lower_word in SMALL_WORDS:
            result.append(lower_word)
            continue

        if "-" in word:
            parts = word.split("-")
            result.append("-".join(p.capitalize() if p else p for p in parts))
            continue

        result.append(word.capitalize())

    return " ".join(result)
