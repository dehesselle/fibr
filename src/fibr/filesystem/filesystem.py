# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from pathlib import Path
import logging

import peewee

from . import db
from .filetype import FileType
from .search import Search

log = logging.getLogger("fs")


class Filesystem:
    def __init__(self):
        self.search = Search()

    def _read_directory(self, directory: Path):
        log.debug(f"directory: {directory}")
        is_root: bool = directory == Path(directory.anchor)
        if not is_root:
            yield {
                db.Files.d_name.column_name: str(directory),
                db.Files.f_mtime.column_name: directory.parent.stat().st_mtime,
                db.Files.f_name.column_name: "..",
                db.Files.f_size.column_name: directory.parent.stat().st_size,
                db.Files.f_type.column_name: FileType.from_path(directory.parent),
            }
        for file in directory.iterdir():
            # this excludes fifo, symlink, junction
            is_file_or_dir: bool = file.is_file() or file.is_dir()
            yield {
                db.Files.d_name.column_name: str(file.parent),
                db.Files.f_mtime.column_name: (
                    file.stat().st_mtime if is_file_or_dir else 0
                ),
                db.Files.f_name.column_name: file.name,
                db.Files.f_size.column_name: (
                    file.stat().st_size if is_file_or_dir else 0
                ),
                db.Files.f_type.column_name: FileType.from_path(file),
            }

    def get_files(self, directory: Path, use_cache: bool = True):
        if use_cache:
            rows = db.select(directory)
            if len(rows):
                # note: an empty directory will never be cached
                return rows

        db.update(self._read_directory(directory), directory)
        return db.select(directory)

    def get_file_id(self, directory: Path, filename: str) -> int:
        try:
            return db.Files.get(
                db.Files.d_name == directory, db.Files.f_name == filename
            ).id
        except peewee.DoesNotExist:
            log.error(f"failed to get ID for {directory} / {filename}")
            return 0

    def get_file_name_by_id(self, id: int) -> str:
        try:
            return db.Files.get(db.Files.id == id).f_name
        except peewee.DoesNotExist:
            log.error(f"failed to get name for id={id}")
            return ""
