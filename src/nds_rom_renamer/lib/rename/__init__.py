import re
from pathlib import Path
from typing import List, Optional, Tuple

from ..common.regions import COUNTRY_REGION_LANGUAGE_MAP, LANGUAGE_CODE_MAP, REGION_CODE_MAP


CONTINENT_REGIONS = {"Europe", "USA", "Asia", "World", "Australia", "Korea", "Japan"}


def sanitize_title(title: str) -> str:
    value = re.sub(r'[<>"/\\|?*]', "", title).strip()
    value = value.replace(":", " -")
    value = re.sub(r"\s+[-]+\s*", " - ", value)
    value = re.sub(r"\s{2,}", " ", value)
    return value.strip()


def map_languages(languages: List[str]) -> List[str]:
    return [LANGUAGE_CODE_MAP.get(code, code) for code in languages]


def resolve_region_language(region: str, languages: List[str]) -> Tuple[str, List[str]]:
    if region in COUNTRY_REGION_LANGUAGE_MAP:
        mapped_region, _ = COUNTRY_REGION_LANGUAGE_MAP[region]
        region_code = mapped_region
    else:
        region_code = REGION_CODE_MAP.get(str(region), str(region).upper() if region else "XX")

    lang_codes = map_languages(languages) if languages else []
    return region_code, lang_codes


def build_filename(title: str, region: str, languages: List[str], serial: str, disc: Optional[str] = None, extra_tags: Optional[List[str]] = None, extension: str = ".nds") -> str:
    clean_title = sanitize_title(title)
    region_code, lang_codes = resolve_region_language(region, languages)
    lang_part = f" [{','.join(lang_codes)}]" if lang_codes else ""

    extra_part = ""
    if extra_tags:
        extra_part = " " + " ".join(f"({sanitize_title(tag)})" for tag in extra_tags)

    ext = extension if extension.startswith(".") else f".{extension}"
    return f"[NDS] {clean_title}{extra_part} [{region_code}]{lang_part} [{serial}]{ext}"


def rename_rom(rom_path: Path, title: str, region: str, languages: List[str], serial: str, disc: Optional[str] = None, extra_tags: Optional[List[str]] = None, dry_run: bool = True) -> Path:
    new_name = build_filename(
        title,
        region,
        languages,
        serial,
        disc=disc,
        extra_tags=extra_tags,
        extension=rom_path.suffix,
    )
    new_path = rom_path.with_name(new_name)

    if new_path.exists() and new_path != rom_path:
        raise FileExistsError(f"Target already exists: {new_path.name}")

    if dry_run:
        print(f"[DRY RUN] {rom_path.name} -> {new_path.name}")
    else:
        rom_path.rename(new_path)
        print(f"Renamed: {rom_path.name} -> {new_path.name}")

    return new_path


def rename_chd(chd_path: Path, title: str, region: str, languages: List[str], serial: str, disc: Optional[str] = None, extra_tags: Optional[List[str]] = None, dry_run: bool = True) -> Path:
    return rename_rom(
        chd_path,
        title,
        region,
        languages,
        serial,
        disc=disc,
        extra_tags=extra_tags,
        dry_run=dry_run,
    )
