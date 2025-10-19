from pathlib import Path
from enum import IntEnum
import logging
import time

from .search import Search
from .files import Files, create_files, delete_files, insert_files, select_files

log = logging.getLogger("fs")


class FileType(IntEnum):
    UNKNOWN = 0
    FILE = 1
    DIR = 2
    LINK = 3
    FIFO = 4


def to_filetype(file: Path) -> FileType:
    if file.is_file():
        return FileType.FILE
    elif file.is_dir():
        return FileType.DIR
    elif file.is_symlink:
        return FileType.LINK
    elif file.is_fifo:
        return FileType.FIFO
    else:
        return FileType.UNKNOWN


class Filesystem:
    def __init__(self):
        create_files()
        self.search = Search()

    def _read_directory(self, directory: Path):
        log.debug(f"directory: {directory}")
        epoch_time = int(time.time())
        is_root: bool = directory == Path(directory.anchor)
        if not is_root:
            yield {
                "d_name": str(directory),
                "f_mtime": directory.parent.stat().st_mtime,
                "f_name": "..",
                "f_size": directory.parent.stat().st_size,
                "f_type": to_filetype(directory.parent),
                "_row_ts": epoch_time,
            }
        for file in directory.iterdir():
            # this excludes fifo, symlink, junction
            is_file_or_dir: bool = file.is_file() or file.is_dir()
            yield {
                "d_name": str(file.parent),
                "f_mtime": file.stat().st_mtime if is_file_or_dir else 0,
                "f_name": file.name,
                "f_size": file.stat().st_size if is_file_or_dir else 0,
                "f_type": to_filetype(file),
                "_row_ts": epoch_time,
            }

    def get(self, directory: Path, use_cache: bool = True):
        if use_cache:
            rows = select_files(directory)
            if len(rows):
                # note: an empty directory will never be cached
                return rows

        delete_files(directory)
        insert_files(self._read_directory(directory))
        return select_files(directory)

    def get_id(self, directory: Path, filename: str) -> int:
        rows = (
            Files.select(Files.id)
            .where(Files.d_name == directory, Files.f_name == filename)
            .tuples()
        )
        if len(rows):
            return rows[0][0]
        else:
            return 0
