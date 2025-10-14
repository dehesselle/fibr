from pathlib import Path
from enum import IntEnum
import logging
from importlib.resources import read_text
import time

from .search import Search
from .db import Files, db

log = logging.getLogger("fs")

SQL_GET_FILES_IN_DIR = read_text("fibr.filesystem", "get_files_in_dir.sql")


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
        self._db_create_table()
        self.search = Search()

    def _db_create_table(self):
        db.create_tables([Files])

    def _db_delete_files(self, directory: Path):
        query = Files.delete().where(Files.d_name == directory)
        _ = query.execute()

    def _db_insert_files(self, rows):
        Files.insert_many(rows).execute()

    def _db_select_files(self, path: Path):
        cursor = db.execute_sql(
            SQL_GET_FILES_IN_DIR,
            (path.as_posix(),),
        )
        rows = cursor.fetchall()
        return rows

    def _read_directory(self, directory: Path):
        log.debug(f"directory: {directory}")
        epoch_time = int(time.time())
        is_root: bool = directory == Path(directory.anchor)
        if not is_root:
            yield {
                "d_name": directory.as_posix(),
                "f_name": "..",
                "f_size": directory.parent.stat().st_size,
                "f_mtime": directory.parent.stat().st_mtime,
                "f_type": to_filetype(directory.parent),
                "_row_ts": epoch_time,
            }
        for file in directory.iterdir():
            # this excludes fifo, symlink, junction
            is_file_or_dir: bool = file.is_file() or file.is_dir()
            yield {
                "d_name": file.parent.as_posix(),
                "f_name": file.name,
                "f_size": file.stat().st_size if is_file_or_dir else 0,
                "f_mtime": file.stat().st_mtime if is_file_or_dir else 0,
                "f_type": to_filetype(file),
                "_row_ts": epoch_time,
            }

    def get(self, path: Path, use_cache: bool = True):
        if use_cache:
            rows = self._db_select_files(path)
            if len(rows):
                return rows

        self._db_delete_files(path)
        self._db_insert_files(self._read_directory(path))
        return self._db_select_files(path)
