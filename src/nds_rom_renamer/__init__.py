import argparse
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

from .lib.identify import extract_serial
from .lib.lookup import get_metadata, load_xml, xml_path
from .lib.rename import rename_rom

BASE_DIR: str = r""


def _iter_rom_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        if path.suffix.lower() in {".nds"}:
            yield path
        return

    for suffix in (".nds"):
        yield from path.rglob(f"*{suffix}")


def run_main(base_dir: Optional[Union[str, Path]] = None, dry_run: bool = True) -> None:
    source_lookup: Dict[str, List[str]] = load_xml(xml_path)

    rom_path = Path(base_dir) if base_dir is not None else Path.cwd()
    rom_files: List[Path] = list(_iter_rom_files(rom_path))

    print(f"Processing {len(rom_files)} file(s)")
    failures: List[tuple[str, str]] = []

    for rom_file in rom_files:
        serial = extract_serial(rom_file)
        if serial is None:
            failures.append((rom_file.name, "no serial found"))
            continue

        metadata: Optional[Dict[str, Any]] = get_metadata(serial, rom_file.stem, source_lookup)
        if metadata is None:
            failures.append((rom_file.name, f"serial {serial} not found in any source"))
            continue

        try:
            rename_rom(
                rom_file,
                metadata["title"],
                metadata["region"],
                metadata.get("languages", []),
                serial,
                disc=metadata.get("disc"),
                extra_tags=metadata.get("extra_tags"),
                dry_run=dry_run,
            )
        except FileExistsError as exc:
            failures.append((rom_file.name, str(exc)))

    if failures:
        print("\nFailed items:")
        for name, reason in failures:
            print(f"  {name}: {reason}")


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Rename Nintendo DS ROM files using GameTDB metadata lookup")
    parser.add_argument("--base-dir", dest="base_dir", default=None, help="Directory containing ROM files")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Preview changes without renaming")
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Apply renames without preview")
    parser.set_defaults(dry_run=True)

    args = parser.parse_args(argv or sys.argv[1:])
    run_main(
        base_dir=args.base_dir if args.base_dir is not None else BASE_DIR,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()