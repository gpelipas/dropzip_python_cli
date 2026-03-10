#!/usr/bin/env python3
"""
Python script to zip files from a source folder and copy the resulting archive to a specified destination folder.


//Run with environment variables as parameters//

export SOURCE_FOLDER=/path/to/source/folder
export DEST_FOLDER=/path/to/destination/folder

# overrides the default value of 'backup' 
# zip will be named backup_YYYYMMDD_HHMMSS.zip
export ZIP_PREFIX=backup    

# overrides the default value of false
export DELETE_AFTER_ZIP=true

# overrides the default value of empty (i.e. all files)
export ZIP_FILE_FILTER=

#.. then run w/o parameters
python dropzip.py 


//Run with parameters//

python dropzip.py --source /data/logs --dest /backups
python dropzip.py --source /data/logs --dest /backups --prefix ZYX
python dropzip.py --source /data/logs --dest /backups --prefix ZYX --delete true
python dropzip.py --source /data/logs --dest /backups --prefix ZYX --delete true --filter ".log"


"""

import os
import zipfile
import logging
import argparse
from datetime import datetime
from pathlib import Path

# == Configuration =============
# Edit these defaults or override them via CLI arguments / environment variables.

SOURCE_FOLDER = os.getenv("ZIP_SOURCE", "/path/to/source/folder")
DEST_FOLDER   = os.getenv("ZIP_DEST",   "/path/to/destination/folder")

# Include a timestamp in the zip filename to avoid overwriting previous archives.
# e.g. backup_20260310_020000.zip
ZIP_PREFIX    = os.getenv("ZIP_PREFIX", "backup")

# Set to True to remove files from source after zipping.
DELETE_AFTER_ZIP = os.getenv("DELETE_AFTER_ZIP", "false").lower() == "true"

# Optional: only zip files matching this extension (e.g. ".log"). Empty = all files.
FILE_EXTENSION_FILTER = os.getenv("ZIP_FILE_FILTER", "")

# == Logging =============
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def collect_files(source: Path, extension_filter: str) -> list[Path]:
    """Return a list of files in *source* (non-recursive) matching the filter."""
    files = [
        f for f in source.iterdir()
        if f.is_file() and (not extension_filter or f.suffix == extension_filter)
    ]
    return files


def create_zip(files: list[Path], zip_path: Path) -> int:
    """Zip *files* into *zip_path*. Returns the number of files zipped."""
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            zf.write(file, arcname=file.name)
            log.info("  + %s", file.name)
    return len(files)


def run(source_folder: str, dest_folder: str,
        zip_prefix: str, delete_after: bool, ext_filter: str) -> None:

    source = Path(source_folder)
    dest   = Path(dest_folder)

    # validate path
    if not source.exists():
        log.error("Source folder does not exist: %s", source)
        raise FileNotFoundError(f"Source folder not found: {source}")

    dest.mkdir(parents=True, exist_ok=True)

    # collect files to be zipped
    files = collect_files(source, ext_filter)
    if not files:
        log.info("No files found in %s (filter=%r).", source,
                 ext_filter or "*")
        return

    log.info("Found %d file(s) in %s", len(files), source)

    # prepare zip filename
    timestamp    = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{zip_prefix}_{timestamp}.zip"
    zip_path     = dest / zip_filename

    # start zipping the files
    log.info("Creating archive: %s", zip_path)
    count = create_zip(files, zip_path)
    log.info("Zipped %d file(s) → %s (%.2f KB)",
             count, zip_path, zip_path.stat().st_size / 1024)

    # delete if specified 
    if delete_after:
        for f in files:
            f.unlink()
            log.info("  - deleted %s", f.name)
        log.info("Deleted %d source file(s).", count)

    log.info("Done.")



# parse CLI parameters
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Zip files from SOURCE and copy the archive to DEST."
    )
    parser.add_argument("--source",  default=SOURCE_FOLDER,
                        help="Folder to zip files from (default: $ZIP_SOURCE)")
    parser.add_argument("--dest",    default=DEST_FOLDER,
                        help="Folder to copy the zip to  (default: $ZIP_DEST)")
    parser.add_argument("--prefix",  default=ZIP_PREFIX,
                        help="Zip filename prefix        (default: 'backup')")
    parser.add_argument("--delete",  action="store_true", default=DELETE_AFTER_ZIP,
                        help="Delete source files after zipping")
    parser.add_argument("--filter",  default=FILE_EXTENSION_FILTER,
                        help="Only zip files with this extension, e.g. '.log'")
    return parser.parse_args()


def main():
    args = parse_args()
    run(
        source_folder=args.source,
        dest_folder=args.dest,
        zip_prefix=args.prefix,
        delete_after=args.delete,
        ext_filter=args.filter,
    )


if __name__ == "__main__":
    main()

