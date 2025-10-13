from pathlib import Path
import sqlite3
from enum import IntEnum
import logging
from importlib.resources import read_text
import time

from .search import Search

log = logging.getLogger("fs")

SQL_CREATE_TABLE = read_text("fibr.filesystem", "create_table.sql")
SQL_INSERT_FILES = read_text("fibr.filesystem", "insert_files.sql")
SQL_GET_FILES_IN_DIR = read_text("fibr.filesystem", "get_files_in_dir.sql")
SQL_DELETE_FILES = read_text("fibr.filesystem", "delete_files.sql")
SQL_SEARCH_FILENAME_LIKE = read_text("fibr.filesystem", "search_filename_like.sql")
SQL_GET_ROWID = read_text("fibr.filesystem", "get_rowid.sql")


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
        _ = self.db.executescript(SQL_CREATE_TABLE)
        _ = self.db.commit()

    def _db_insert(self, rows):
        _ = self.db.executemany(SQL_INSERT_FILES, rows)
        _ = self.db.commit()

    def _db_delete(self, directory: Path):
        _ = self.db.execute(SQL_DELETE_FILES, {"d_name": directory.as_posix()})
        _ = self.db.commit()

    def _db_select(self, path: Path):
        cursor = self.db.execute(
            SQL_GET_FILES_IN_DIR,
            {"d_name": path.as_posix()},
        )
        rows = cursor.fetchall()
        return rows

    def _db_get_rowid(self, directory: str, filename: str) -> int:
        cursor = self.db.execute(
            SQL_GET_ROWID,
            {"d_name": directory, "f_name": filename},
        )
        row = cursor.fetchone()
        return row[0]

    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self._db_create_table()
        self.search = Search(self.db)

    def get_files(self, directory: Path):
        log.debug(f"         directory: {directory}")
        directory = directory.resolve()
        log.debug(f"resolved directory: {directory}")
        epoch_time = int(time.time())
        is_root: bool = directory == Path(directory.anchor)
        if not is_root:
            yield {
                "d_name": directory.as_posix(),
                "f_name": "..",
                "f_size": directory.parent.stat().st_size,
                "f_modified": directory.parent.stat().st_mtime,
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
                "f_modified": file.stat().st_mtime if is_file_or_dir else 0,
                "f_type": to_filetype(file),
                "_row_ts": epoch_time,
            }

    def get(self, path: Path, use_cache: bool = True):
        if use_cache:
            rows = self._db_select(path)
            if len(rows):
                return rows

        self._db_delete(path)
        self._db_insert(self.get_files(path))
        rows = self._db_select(path)
        return rows
