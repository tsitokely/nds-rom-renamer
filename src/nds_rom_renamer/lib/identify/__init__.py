from pathlib import Path
from .rom_util import extract_serial_from_rom


def extract_serial(rom_path: Path, poll_interval: float = 0.2) -> str | None:
    suffix = rom_path.suffix.lower()
    return extract_serial_from_rom(rom_path)
