from importlib.resources import read_text
from pathlib import Path
import logging

from peewee import Model, CharField, IntegerField, SqliteDatabase, fn
from sqlite3 import Cursor

db = SqliteDatabase(":memory:")
log = logging.getLogger("fs")

SQL_GET_FILES_IN_DIR = " ".join(
    [_.strip() for _ in read_text("fibr.filesystem", "get_files_in_dir.sql").split()]
)
SQL_UPSERT_FILES_FROM_STAGING = " ".join(
    [
        _.strip()
        for _ in read_text("fibr.filesystem", "upsert_files_from_staging.sql").split()
    ]
)


class Files(Model):
    d_name = CharField()  # canonical
    f_mtime = IntegerField()  # TODO: datetime?
    f_name = CharField()
    f_size = IntegerField()
    f_type = IntegerField()

    class Meta:
        database = db
        indexes = ((("d_name", "f_name"), True),)


class FilesStaging(Files):
    pass


def create_files() -> None:
    db.create_tables([Files, FilesStaging])


def update_files(rows, directory: Path) -> None:
    # read directory content into filesstaging table
    FilesStaging.truncate_table()
    FilesStaging.insert_many(rows).execute()
    # upsert files table with records from filesstaging table
    cursor: Cursor = db.execute_sql(SQL_UPSERT_FILES_FROM_STAGING)
    log.debug(f"upserted {cursor.rowcount} records")
    # delete all files for which are not in staging for given directory
    composite_key_in_staging = FilesStaging.select().where(
        FilesStaging.d_name == Files.d_name, FilesStaging.f_name == Files.f_name
    )
    delete_count = (
        Files.delete()
        .where(~fn.EXISTS(composite_key_in_staging), Files.d_name == directory)
        .execute()
    )
    log.debug(f"deleted {delete_count} records")


def select_files(directory: Path) -> list:
    cursor = db.execute_sql(
        SQL_GET_FILES_IN_DIR,
        (str(directory),),
    )
    rows = cursor.fetchall()
    return rows
