# NDS ROM Renamer

A lightweight utility for renaming Nintendo DS ROM files to a cleaner, more consistent format based on their metadata and game titles.

## Overview

This project helps you organize your Nintendo DS game collection by automatically renaming `.nds` files into a readable naming scheme. It is useful for users who want to keep their ROM library tidy and easier to browse.

## Features

- Renames Nintendo DS ROMs from raw filenames to cleaner names
- Preserves important game metadata when available
- Supports batch renaming of multiple ROM files
- Helps keep folder contents consistent and easier to manage
- Simple command-line workflow

## Requirements

- Python 3.9+
- uv installed (`pip install uv` or `brew install uv`)
- A filesystem with access to the ROM directory

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/nds-rom-renamer.git
   cd nds-rom-renamer
   ```

2. Create and sync the project environment with uv:

   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```

3. If you prefer to run commands without activating the virtual environment:

   ```bash
   uv run python main.py /path/to/roms
   ```

## Usage

Run the renamer against a folder containing ROM files:

```bash
uv run python main.py /path/to/roms
```

You can also pass an optional output directory or custom naming pattern if supported by your implementation.

Example:

```bash
uv run python main.py "./roms" --dry-run
```

The tool will scan files, detect game names, and display the intended renamed output before applying changes.

## Project Structure

```text
nds-rom-renamer/
├── main.py
├── renamer.py
├── README.md
└── ...
```

## Notes

- Always make backups before renaming ROM files.
- Check the output carefully before confirming batch renames.
- This project is intended for personal library management and does not distribute copyrighted game files.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with a clear description of the changes.
