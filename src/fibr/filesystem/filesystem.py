from pathlib import Path
import sqlite3
from enum import IntEnum
from importlib.resources import read_text
import time

from .search import Search

SQL_CREATE_TABLE = read_text("fibr.filesystem", "create_table.sql")
SQL_INSERT_FILES = read_text("fibr.filesystem", "insert_files.sql")
SQL_GET_FILES_IN_DIR = read_text("fibr.filesystem", "get_files_in_dir.sql")
SQL_DELETE_FILES = read_text("fibr.filesystem", "delete_files.sql")
SQL_SEARCH_FILENAME_LIKE = read_text("fibr.filesystem", "search_filename_like.sql")


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
    def _db_create_table(self):
        _ = self.db.execute(SQL_CREATE_TABLE)

    def _db_insert(self, rows):
        _ = self.db.executemany(SQL_INSERT_FILES, rows)

    def _db_select(self, path: Path):
        cursor = self.db.execute(
            SQL_GET_FILES_IN_DIR,
            path.as_posix(),
        )
        rows = cursor.fetchall()
        return rows

    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self._db_create_table()
        self.search = Search(self.db)

    def get_files(self, path: Path):
        epoch_time = int(time.time())
        yield {
            "d_name": path.as_posix(),
            "f_name": "..",
            "f_size": path.parent.stat().st_size,
            "f_modified": path.parent.stat().st_mtime,
            "f_type": to_filetype(path.parent),
            "_row_ts": epoch_time,
        }
        for file in path.iterdir():
            yield {
                "d_name": file.parent.as_posix(),
                "f_name": file.name,
                "f_size": file.stat().st_size,
                "f_modified": file.stat().st_mtime,
                "f_type": to_filetype(file),
                "_row_ts": epoch_time,
            }

    def get(self, path: Path, reload: bool = False):
        if not reload:
            rows = self._db_select(path)
            if len(rows):
                return rows

        self._db_insert(self.get_files(path))
        rows = self._db_select(path)
        return rows
