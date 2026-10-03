from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
ASSETS_DIR = PROJECT_ROOT / "assets"

gametdb_db = ASSETS_DIR / "dstdb.xml"

__all__ = ["PROJECT_ROOT", "ASSETS_DIR", "gametdb_db"]