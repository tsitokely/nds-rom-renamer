import xml.etree.ElementTree as ET
from pathlib import Path
from .utils import DISC_PATTERN, PAREN_PATTERN


_REGION_ALIASES = {
    "USA": "USA",
    "US": "USA",
    "NTSC-U": "USA",
    "NORTH AMERICA": "USA",
    "EUROPE": "EUR",
    "EUR": "EUR",
    "EU": "EUR",
    "PAL": "EUR",
    "JAPAN": "JPN",
    "JP": "JPN",
    "NTSC-J": "JPN",
    "KOREA": "KOR",
    "KR": "KOR",
    "NTSC-K": "KOR",
    "AUSTRALIA": "AUS",
    "AUS": "AUS",
    "CHINA": "CHN",
    "CHN": "CHN",
    "FRANCE": "FRA",
    "FRA": "FRA",
    "GERMANY": "GER",
    "GER": "GER",
    "SPAIN": "ESP",
    "ESP": "ESP",
    "ITALY": "ITA",
    "ITA": "ITA",
}


def _normalize_region_tag(tag: str, region_map: dict) -> str | None:
    clean = tag.strip()
    if not clean:
        return None

    lookup_key = clean.upper()
    if clean in region_map:
        return clean
    if lookup_key in region_map:
        return lookup_key

    alias = _REGION_ALIASES.get(clean)
    if alias:
        return alias

    alias = _REGION_ALIASES.get(lookup_key)
    if alias:
        return alias

    normalized = clean.replace("-", " ").replace("_", " ").strip()
    return _REGION_ALIASES.get(normalized.upper())


def load_source_data(dat_path: str) -> dict:
    tree = ET.parse(dat_path)
    root = tree.getroot()
    lookup = {}

    for game in root.findall("game"):
        serial_elem = game.find("id")
        if serial_elem is None or not serial_elem.text:
            continue

        serial = serial_elem.text.strip()
        title = (game.get("name") or "").strip()

        if not title:
            locale = game.find("locale")
            if locale is not None:
                locale_title = locale.find("title")
                if locale_title is not None and locale_title.text:
                    title = locale_title.text.strip()

        if not title:
            rom_elem = game.find("rom")
            if rom_elem is not None:
                title = (rom_elem.get("name") or "").strip()

        if title:
            lookup.setdefault(serial, []).append(title)

    return lookup


def parse_source_name(name: str, region_map: dict, is_language_tag_fn) -> dict:
    disc_match = DISC_PATTERN.search(name)
    disc_number = disc_match.group(1) if disc_match else None

    name_no_disc = DISC_PATTERN.sub("", name)
    title = name_no_disc.split("(")[0].strip()

    tags = PAREN_PATTERN.findall(name_no_disc)

    region = None
    languages = []
    extra_tags = []
    for i, tag in enumerate(tags):
        tag = tag.strip()
        if not tag:
            continue

        normalized_region = _normalize_region_tag(tag, region_map)
        if normalized_region is not None:
            if region is None:
                region = normalized_region
            continue

        if is_language_tag_fn(tag):
            languages = [p.strip() for p in tag.split(",")]
            continue

        extra_tags.append(tag)

    region_code = region_map.get(region, region)
    if region_code is not None:
        region = region_code

    formatted_parts = [title]
    for t in extra_tags:
        formatted_parts.append(f"({t})")
    if disc_number:
        formatted_parts.append(f"(Disc {disc_number})")
    if region_code:
        formatted_parts.append(f"[{region_code}]")

    formatted_title = " ".join(formatted_parts)

    return {
        "title": title,
        "region": region,
        "languages": languages,
        "disc": disc_number,
        "extra_tags": extra_tags,
        "formatted_title": formatted_title,
    }
