# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging

from peewee import fn

from .db import Files

log = logging.getLogger("fs")


class Search:
    def __init__(self):
        self.results = list()
        self.index = -1

    def _search_files_like(self, directory: str, filename: str) -> None:
        self.results = [
            row[0]
            for row in Files.select(
                Files.id  # pyright: ignore[reportAttributeAccessIssue]
                # this is a Pylance deficiency, see related issue
                # https://github.com/microsoft/pylance-release/issues/3701
            )
            .where(
                fn.LOWER(Files.f_name).startswith(filename.lower()),
                Files.d_name == directory,
            )
            .tuples()
        ]
        self.index = -1

    def next(self, directory: str = "", filename: str = "") -> int:
        if directory:
            self._search_files_like(directory, filename)

        if len(self.results):
            self.index += 1
            if not self.index < len(self.results):
                self.index = 0
            return self.results[self.index]
        else:
            return 0

    def previous(self, directory: str = "", filename: str = "") -> int:
        if directory:
            self._search_files_like(directory, filename)

        if len(self.results):
            self.index -= 1
            if not self.index > -1:
                self.index = len(self.results) - 1

            return self.results[self.index]
        else:
            return 0
