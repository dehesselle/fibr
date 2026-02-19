# SPDX-FileCopyrightText: 2026 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from configparser import ConfigParser
from typing import Union

from .configoption import ConfigOption

log = logging.getLogger("config")


class ConfigSection:
    def __init__(self, config: ConfigParser, section: str):
        self.section = section
        self.config = config
        if not config.has_section(self.section):
            config.add_section(self.section)

    def __getitem__(self, option: str) -> str:
        try:
            return self.config[self.section][option]
        except KeyError:
            return ""

    def __setitem__(self, option: str, value: str) -> None:
        self.config[self.section][option] = str(value)

    def new[T](
        self, option: str, default: Union[T, tuple[T, T, T]] = str
    ) -> ConfigOption[T]:
        if isinstance(default, tuple):
            return ConfigOption[T](
                self.config[self.section], option
            ).set_default_by_platform(*default)
        else:
            return ConfigOption[T](self.config[self.section], option).set_default(
                default
            )
