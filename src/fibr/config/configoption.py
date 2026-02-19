# SPDX-FileCopyrightText: 2026 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
import os
import platform
from configparser import SectionProxy
from enum import IntEnum
from pathlib import Path
from typing import Self, Union

log = logging.getLogger("config")


class ConfigOption[T]:
    class Platform(IntEnum):
        darwin = 0
        linux = 1
        windows = 2

    def __init__(self, section: SectionProxy, name: str) -> None:
        self.section = section
        self.name = name
        self.env_name = ""
        self._default: Union[T, tuple[T, T, T]]

    def set_default(self, default: T) -> Self:
        self._default = default
        return self

    def set_default_by_platform(self, darwin: T, linux: T, windows: T) -> Self:
        self._default = (darwin, linux, windows)
        return self

    def set_env_name(self, env_name: str) -> Self:
        self.env_name = env_name
        return self

    @property
    def default(self) -> T:
        if isinstance(self._default, tuple):
            # TODO: handle unsupported platforms?
            return self._default[self.Platform[platform.system().lower()]]
        else:
            return self._default

    @property
    def value(self) -> str:
        result = ""
        if self.env_name:  # environment variables take priority
            result = os.getenv(self.env_name)
        if not result:  # otherwise get from file or default
            try:
                result = self.section[self.name]
            except KeyError:
                self.section[self.name] = result = str(self.default)
        return result

    @property
    def as_int(self) -> int:
        if isinstance(self.default, int):
            return int(self.value)
        else:
            raise TypeError(f"{self.name} is not an int")

    @property
    def as_str(self) -> str:
        return self.value

    @property
    def as_bool(self) -> bool:
        if isinstance(self.default, bool):
            return bool(self.value)
        else:
            raise TypeError(f"{self.name} is not a bool")

    @property
    def as_path(self) -> Path:
        if isinstance(self.default, Path):
            return Path(self.value)
        else:
            raise TypeError(f"{self.name} is not a Path")
