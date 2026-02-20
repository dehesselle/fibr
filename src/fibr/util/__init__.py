# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from .convert import bytes_to_str, epoch_to_str
from .log import setup_logging
from .platform import is_linux, is_macos, is_windows
from .version import VERSION
