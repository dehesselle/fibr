# SPDX-FileCopyrightText: 2026 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
import platform
from dataclasses import dataclass, field
from typing import Any, Optional, Union

log = logging.getLogger("config")


@dataclass
class DefaultByPlatform:
    darwin: Any
    linux: Any
    windows: Any


@dataclass
class ConfigOption:
    name: str
    default_value: Union[DefaultByPlatform, Any]  # pyright: ignore[reportRedeclaration]
    env_name: Optional[str] = ""
    _default_value: Union[DefaultByPlatform, Any] = field(init=False, repr=False)

    @property
    def default_value(self):
        if isinstance(self._default_value, DefaultByPlatform):
            # TODO: handle unsupported platform
            return getattr(self._default_value, platform.system().lower())
        else:
            return self._default_value

    @default_value.setter
    def default_value(self, value) -> None:
        self._default_value = value
