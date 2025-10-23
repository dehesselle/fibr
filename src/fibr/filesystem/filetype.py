# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from enum import IntEnum, auto
from pathlib import Path


class FileType(IntEnum):
    UNKNOWN = 0
    FILE = auto()
    DIR = auto()
    LINK = auto()
    FIFO = auto()

    @classmethod
    def from_path(cls, file: Path):
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
