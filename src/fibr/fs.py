from pathlib import Path
import sqlite3
from enum import StrEnum


class NotFoundException(Exception):
    """Exception raised for search not yielding any result."""


def get_fs_obj(path: Path):
    for obj in path.iterdir():
        yield {
            "directory": "foo",
            "name": obj.name,
            "size": obj.stat().st_size,
            "modify": obj.stat().st_mtime,
        }


class FsDb:
    class ObjectType(StrEnum):
        FILE = "file"
        DIR = "directory"
        LINK = "link"

    def create_table(self):
        self.db.execute(
            "CREATE TABLE files(directory TEXT, name TEXT, size INTEGER, modify INTEGER)"
        )

    def add_files(self, the_list):
        cur = self.db.executemany(
            "INSERT INTO files VALUES(:directory, :name, :size, :modify)", the_list
        )

    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.create_table()

    def get_fs_obj(self, path: Path):  # -> List[Path]:
        for obj in path.iterdir():
            yield {
                "directory": obj.parent.as_posix(),
                "name": obj.name,
                "size": obj.stat().st_size,
                "modify": obj.stat().st_mtime,
            }

    def get(self, path: Path, refresh: bool = False):
        if not refresh:
            cur = self.db.execute(
                "SELECT rowid, name, size, modify FROM files WHERE directory = :directory",
                [path.as_posix()],
            )
            rows = cur.fetchall()
            if len(rows):
                return rows

        # FIXME: need to drop old records first
        self.add_files(self.get_fs_obj(path))
        cur = self.db.execute(
            "SELECT rowid, name, size, modify FROM files WHERE directory = :directory",
            [path.as_posix()],
        )
        rows = cur.fetchall()
        return rows

    def get_rowid(self, path: Path, name: str):
        cur = self.db.execute(
            "SELECT rowid FROM files WHERE directory = :directory AND name LIKE :name",
            [path.as_posix(), name + "%"],
        )
        rows = cur.fetchone()
        if rows:
            return str(rows[0])
        else:
            raise NotFoundException()
