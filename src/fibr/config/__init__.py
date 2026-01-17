# SPDX-FileCopyrightText: 2026 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from configparser import ConfigParser

from .configfile import ConfigFile
from .configsection import ConfigSection

config = ConfigParser()
config_file = ConfigFile(config)  # provides automatic save/load


def get_section(section: str) -> ConfigSection:
    return ConfigSection(config, section)
