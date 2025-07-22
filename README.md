# EXIF Finder

EXIF Finder is a command-line tool for locating JPEG images by their EXIF date. It recursively searches a given directory and lists files whose `DateTimeOriginal` or `CreateDate` metadata matches a specified date.

## Features

- Fast scanning without decoding full image data
- Handles Unicode paths
- Optional output to a file
- Works on Windows, macOS and Linux

## Installation

Install the required dependency and run the tool:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m exif_finder --path "/path/to/photos" --date 2012-09-03
```

Options:

- `--path`: root directory to search
- `--date`: date in `YYYY-MM-DD` format to match
- `--output`: write results to a UTF-8 file
- `--include-date`: include the matched date before each path
- `--verbose`: print every processed file and debug info
- `--only-folders`: output only folders of matches without duplicates

Example with output file:

```bash
python -m exif_finder --path C:\Photos --date 2012-09-03 --output results.txt --include-date
```

## License

This project is licensed under the MIT License.
