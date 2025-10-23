# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path
from typing import List, Tuple

from peewee import Model, CharField, IntegerField, SqliteDatabase, fn, JOIN, Case

from .filetype import FileType

db = SqliteDatabase(":memory:")
log = logging.getLogger("fs")


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


def update(rows, directory: Path) -> None:
    # read directory content into FilesStaging table
    FilesStaging.truncate_table()
    FilesStaging.insert_many(rows).execute()

    # upsert rows: FilesStaging -> Files
    upsert_count = (
        Files.insert_from(
            FilesStaging.select(
                FilesStaging.d_name,
                FilesStaging.f_mtime,
                FilesStaging.f_name,
                FilesStaging.f_size,
                FilesStaging.f_type,
            ).join(
                Files,
                JOIN.LEFT_OUTER,
                on=(
                    (FilesStaging.d_name == Files.d_name)
                    & (FilesStaging.f_name == Files.f_name)
                ),
            ),
            fields=[
                Files.d_name,
                Files.f_mtime,
                Files.f_name,
                Files.f_size,
                Files.f_type,
            ],
        )
        .on_conflict(
            conflict_target=[Files.d_name, Files.f_name],
            preserve=[
                Files.f_mtime,
                Files.f_size,
                Files.f_type,
            ],
        )
        .execute()
    )
    log.debug(f"upserted {upsert_count} records")

    # delete all rows in Files which are not in FilesStaging for
    # the given directory
    delete_count = (
        Files.delete()
        .where(
            ~fn.EXISTS(
                FilesStaging.select().where(
                    FilesStaging.d_name == Files.d_name,
                    FilesStaging.f_name == Files.f_name,
                )
            ),
            Files.d_name == directory,
        )
        .execute()
    )
    log.debug(f"deleted {delete_count} records")


def select(directory: Path) -> List[Tuple[int, ...]]:
    directories_first = Case(None, [(Files.f_type == FileType.DIR, 1)], 2)
    return (
        Files.select(
            Files.id, Files.f_name, Files.f_size, Files.f_mtime, directories_first
        )
        .where(Files.d_name == directory)
        .order_by(directories_first, Files.f_name)
        .tuples()
    )


db.create_tables([Files, FilesStaging])
