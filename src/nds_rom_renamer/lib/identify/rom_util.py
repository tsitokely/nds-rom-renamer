from pathlib import Path
from typing import Optional


def extract_serial_from_rom(rom_path: Path, read_size: int = 0x100) -> Optional[str]:
    with open(rom_path, "rb") as f:
        header = f.read(read_size)

    if len(header) < 0x10:
        return None

    game_code = header[0x0C:0x10].decode("ascii", errors="ignore").strip("\x00")
    if len(game_code) == 4:
        return game_code

    return None
