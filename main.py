"""Front page for 26 November 2026, delivered to the grader.

The day's news was drawn into entry.png before this program runs.
All this program does is place that finished picture where the
competition expects it, using only the Python standard library.
"""

import os
import sys
from pathlib import Path


def find_front_page() -> Path:
    """Locate the picture bundled beside this file."""
    picture = Path(__file__).resolve().parent / "entry.png"
    if not picture.is_file():
        sys.exit(f"entry.png is missing next to {__file__}")
    return picture


def output_folder() -> Path:
    """Return the grader's output folder, creating it if needed."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    folder = Path(wanted)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def place_picture(picture: Path, folder: Path) -> Path:
    """Stream the picture into the folder in 64 KiB blocks."""
    target = folder / "entry.png"
    with picture.open("rb") as reader, target.open("wb") as writer:
        while True:
            block = reader.read(65536)
            if not block:
                break
            writer.write(block)
    if target.stat().st_size != picture.stat().st_size:
        sys.exit(f"copy incomplete: {target} is not the same size as {picture}")
    return target


def main() -> None:
    picture = find_front_page()
    delivered = place_picture(picture, output_folder())
    print(f"wrote {delivered}")


if __name__ == "__main__":
    main()
