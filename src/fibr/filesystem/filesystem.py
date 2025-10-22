from pathlib import Path
from enum import IntEnum, auto
import logging

from .search import Search
from .files import Files, create_files, update_files, select_files

log = logging.getLogger("fs")


class FileType(IntEnum):
    UNKNOWN = 0
    FILE = auto()
    DIR = auto()
    LINK = auto()
    FIFO = auto()


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
        is_root: bool = directory == Path(directory.anchor)
        if not is_root:
            yield {
                Files.d_name.column_name: str(directory),
                Files.f_mtime.column_name: directory.parent.stat().st_mtime,
                Files.f_name.column_name: "..",
                Files.f_size.column_name: directory.parent.stat().st_size,
                Files.f_type.column_name: to_filetype(directory.parent),
            }
        for file in directory.iterdir():
            # this excludes fifo, symlink, junction
            is_file_or_dir: bool = file.is_file() or file.is_dir()
            yield {
                Files.d_name.column_name: str(file.parent),
                Files.f_mtime.column_name: (
                    file.stat().st_mtime if is_file_or_dir else 0
                ),
                Files.f_name.column_name: file.name,
                Files.f_size.column_name: file.stat().st_size if is_file_or_dir else 0,
                Files.f_type.column_name: to_filetype(file),
            }

    def get(self, directory: Path, use_cache: bool = True):
        if use_cache:
            rows = select_files(directory)
            if len(rows):
                # note: an empty directory will never be cached
                return rows

        update_files(self._read_directory(directory), directory)
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

    def get_name_by_id(self, id: int) -> str:
        try:
            return Files.select(Files.f_name).where(Files.id == id).tuples()[0][0]
        except IndexError as e:
            log.error(f"failed to get name for id={id}")
            return ""
