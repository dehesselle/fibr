# SPDX-FileCopyrightText: 2026 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import atexit
from configparser import ConfigParser
from pathlib import Path

import platformdirs


class ConfigFile:
    def __init__(self, config_parser: ConfigParser):
        self.config_parser = config_parser
        self.file = (
            Path(
                platformdirs.user_config_dir(
                    appauthor=False,
                    appname="fibr",
                    ensure_exists=True,
                )
            )
            / "config.ini"
        )
        self.load()
        atexit.register(self.save)

    def load(self) -> None:
        if self.file.exists():
            self.config_parser.read(self.file)

    def save(self) -> None:
        self.file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file, "wt") as file:
            self.config_parser.write(file)
