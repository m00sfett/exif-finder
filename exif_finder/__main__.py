from __future__ import annotations

import argparse
import datetime as _dt
import os
from pathlib import Path
from typing import Iterable, Optional, Set

from PIL import Image, ExifTags


DATE_TAGS = [
    tag for tag, name in ExifTags.TAGS.items() if name in {"DateTimeOriginal", "CreateDate"}
]


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find JPEG images by EXIF date")
    parser.add_argument(
        "--path", required=True, help="Root directory to search"
    )
    parser.add_argument(
        "--date",
        required=True,
        help="Date to match in format YYYY-MM-DD",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Optional file to write results (UTF-8)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show every processed file and debug details",
    )
    parser.add_argument(
        "--only-folders",
        action="store_true",
        help="Output only folders of matches without duplicates",
    )
    parser.add_argument(
        "--include-date",
        action="store_true",
        help="Include matched date in output",
    )
    return parser.parse_args(argv)


def iter_jpeg_files(root: Path) -> Iterable[Path]:
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.lower().endswith((".jpg", ".jpeg")):
                yield Path(dirpath) / name


def exif_date(path: Path) -> Optional[str]:
    try:
        with Image.open(path) as im:
            exif = im.getexif()
            for tag in DATE_TAGS:
                value = exif.get(tag)
                if value:
                    # value might be "YYYY:MM:DD HH:MM:SS"
                    return str(value)
    except Exception:
        return None
    return None


def match_date(date_text: str, expected: _dt.date) -> bool:
    try:
        parts = date_text.split()[0].replace(":", "-")
        return _dt.date.fromisoformat(parts) == expected
    except Exception:
        return False


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    root = Path(args.path)
    target_date = _dt.date.fromisoformat(args.date)
    output_file = None
    if args.output:
        output_path = Path(args.output)
        output_file = output_path.open("w", encoding="utf-8")
    printed_folders: Set[str] = set()

    for file in iter_jpeg_files(root):
        if args.verbose:
            print(f"Checking {file}")
        date_text = exif_date(file)
        if args.verbose:
            print(f"  EXIF date: {date_text}")
        if date_text and match_date(date_text, target_date):
            if args.only_folders:
                line_path = str(file.parent)
                if line_path in printed_folders:
                    continue
                printed_folders.add(line_path)
            else:
                line_path = str(file)

            line = line_path
            if args.include_date:
                line = f"{target_date.isoformat()}: {line}"
            print(line)
            if output_file:
                output_file.write(line + "\n")

    if output_file:
        output_file.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
