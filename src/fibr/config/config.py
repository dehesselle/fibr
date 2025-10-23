# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import configparser
from pathlib import Path
import platformdirs

MAIN_SECTION = "main"
config = configparser.ConfigParser()
ini_file = (
    Path(
        platformdirs.user_config_dir(
            appauthor=False,
            appname="fibr",
            ensure_exists=True,
        )
    )
    / "config.ini"
)


def load() -> None:
    if ini_file.exists():
        config.read(ini_file)
    else:
        config.add_section(MAIN_SECTION)


def save() -> None:
    ini_file.parent.mkdir(parents=True, exist_ok=True)
    with open(ini_file, "w") as file:
        config.write(file)


def getInt(option: str, fallback: int = -1, section: str = MAIN_SECTION) -> int:
    try:
        return config.getint(section, option)
    except configparser.NoOptionError:
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, option, str(fallback))
    return config.getint(section, option)


def getStr(option: str, fallback: str = "", section: str = MAIN_SECTION) -> str:
    try:
        return config.get(section, option)
    except configparser.NoOptionError:
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, option, fallback)
    return config.get(section, option)


def exists(option: str, section: str = MAIN_SECTION) -> bool:
    return config.has_option(section, option)
