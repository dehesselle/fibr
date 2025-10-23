# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging

from .db import Files
from peewee import fn

log = logging.getLogger("fs")


class Search:
    def __init__(self):
        self.results = list()
        self.index = -1

    def _search_files_like(self, directory: str, filename: str):
        self.results = [
            row[0]
            for row in Files.select(Files.id)
            .where(
                fn.LOWER(Files.f_name).startswith(filename.lower()),
                Files.d_name == directory,
            )
            .tuples()
        ]
        self.index = -1

    def next(self, directory: str = None, filename: str = None) -> int:
        if directory:
            self._search_files_like(directory, filename)

        if len(self.results):
            self.index += 1
            if not self.index < len(self.results):
                self.index = 0

            return self.results[self.index]
        else:
            return 0

    def previous(self, directory: str = None, filename: str = None) -> int:
        if directory:
            self.results = self._search_files_like(directory, filename)
            self.index = -1

        if len(self.results):
            self.index -= 1
            if not self.index > -1:
                self.index = len(self.results) - 1

            return self.results[self.index]
        else:
            return 0
