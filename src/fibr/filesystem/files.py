from importlib.resources import read_text
from pathlib import Path
import logging

from peewee import Model, CharField, IntegerField, SqliteDatabase

db = SqliteDatabase(":memory:")
log = logging.getLogger("fs")

SQL_GET_FILES_IN_DIR = " ".join(
    [_.strip() for _ in read_text("fibr.filesystem", "get_files_in_dir.sql").split()]
)


class Files(Model):
    d_name = CharField()  # canonical
    f_mtime = IntegerField()  # TODO: datetime?
    f_name = CharField()
    f_size = IntegerField()
    f_type = IntegerField()
    _row_ts = IntegerField()  # TODO: datetime?

    class Meta:
        database = db
        indexes = ((("d_name", "f_name"), True),)


def create_files() -> None:
    db.create_tables([Files])


def delete_files(directory: Path) -> None:
    query = Files.delete().where(Files.d_name == directory)
    _ = query.execute()
    log.debug(f"deleted {_} records")


def insert_files(rows) -> None:
    Files.insert_many(rows).execute()


def select_files(directory: Path) -> list:
    cursor = db.execute_sql(
        SQL_GET_FILES_IN_DIR,
        (str(directory),),
    )
    rows = cursor.fetchall()
    return rows
