from pathlib import Path
from enum import IntEnum
import logging
from importlib.resources import read_text
import time

from .search import Search
from .db import Files, db

log = logging.getLogger("fs")

SQL_GET_FILES_IN_DIR = " ".join(
    [_.strip() for _ in read_text("fibr.filesystem", "get_files_in_dir.sql").split()]
)


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

    def _db_create_table(self) -> None:
        db.create_tables([Files])

    def _db_delete_files(self, directory: Path) -> None:
        query = Files.delete().where(Files.d_name == directory)
        _ = query.execute()
        log.debug(f"deleted {_} records")

    def _db_insert_files(self, rows) -> None:
        Files.insert_many(rows).execute()

    def _db_select_files(self, directory: Path) -> list:
        cursor = db.execute_sql(
            SQL_GET_FILES_IN_DIR,
            (str(directory),),
        )
        rows = cursor.fetchall()
        return rows

    def _read_directory(self, directory: Path):
        log.debug(f"directory: {directory}")
        epoch_time = int(time.time())
        is_root: bool = directory == Path(directory.anchor)
        if not is_root:
            yield {
                "d_name": str(directory),
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
                "d_name": str(file.parent),
                "f_name": file.name,
                "f_size": file.stat().st_size if is_file_or_dir else 0,
                "f_mtime": file.stat().st_mtime if is_file_or_dir else 0,
                "f_type": to_filetype(file),
                "_row_ts": epoch_time,
            }

    def get(self, directory: Path, use_cache: bool = True):
        if use_cache:
            rows = self._db_select_files(directory)
            if len(rows):
                # note: an empty directory will never be cached
                return rows

        self._db_delete_files(directory)
        self._db_insert_files(self._read_directory(directory))
        return self._db_select_files(directory)

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
