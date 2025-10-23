# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from datetime import datetime


def epoch_to_str(epoch: int) -> str:
    dt = datetime.fromtimestamp(epoch)
    if dt.year == datetime.now().year:
        return dt.strftime("%b %d %H:%M")
    else:
        return dt.strftime("%b %d %Y")


def bytes_to_str(bytes: int) -> str:
    if bytes > 9999999:
        kb = int(bytes / 1024)
        if kb > 999999:
            mb = int(kb / 1024)
            if mb > 9999999:
                gb = int(mb / 1024)
                return (str(gb) + "G").rjust(7)
            else:
                return (str(mb) + "M").rjust(7)
        else:
            return (str(kb) + "K").rjust(7)
    else:
        return str(bytes).rjust(7)
