from typing import Optional

from ..common.assets import gametdb_db
from ..common.regions import REGION_CODE_MAP
from .gametdb import load_source_data, parse_source_name
from .utils import is_language_tag

# defaults used by root-level wrapper
xml_path = gametdb_db
DAT_PATH = str(gametdb_db)


def load_xml(path) -> dict:
    return load_source_data(str(path))


def get_metadata(serial: str, original_name: str = "", source_lookup: Optional[dict] = None) -> Optional[dict]:
    if source_lookup is None:
        source_lookup = load_source_data(DAT_PATH)

    names = source_lookup.get(serial)
    if names:
        if original_name:
            best = max(names, key=lambda n: len(set(n.lower().split()) & set(original_name.lower().split())))
            return parse_source_name(best, REGION_CODE_MAP, is_language_tag)
        return parse_source_name(names[0], REGION_CODE_MAP, is_language_tag)

    return None
