# SPDX-FileCopyrightText: 2026 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from configparser import ConfigParser
from pathlib import Path
import logging
import os
from .configoption import ConfigOption
from dacite import from_dict

log = logging.getLogger("config")


class ConfigSection:
    def __init__(self, config: ConfigParser, section: str):
        self.section = section
        self.config = config
        if not config.has_section(self.section):
            config.add_section(self.section)

    def __getitem__(self, option: dict) -> bool | int | str | Path:
        return self.get_value(from_dict(ConfigOption, option))

    def __setitem__(self, option: str, value: bool | int | str | Path) -> None:
        self.config[self.section][option] = str(value)

    def getint(self, option: str) -> int | None:
        return self.config.getint(self.section, option)

    def getboolean(self, option: str) -> bool | None:
        return self.config.getboolean(self.section, option)

    def get_value(self, option: ConfigOption) -> bool | int | str | Path:
        value = ""
        if option.env_name:  # environment variables take priority
            value = os.getenv(option.env_name)
        if not value:  # otherwise get from file or default
            if not self.config.has_option(self.section, option.name):
                self.config[self.section][option.name] = str(option.default_value)
            value = self.config[self.section][option.name]

        if isinstance(option.default_value, int):
            return int(value)
        elif isinstance(option.default_value, bool):
            return bool(value != "False")
        elif isinstance(option.default_value, Path):
            return Path(value)
        else:
            return str(value)
