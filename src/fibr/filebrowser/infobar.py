# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging

from textual.events import Resize
from textual.widgets import Static
from textual import on

log = logging.getLogger("panel")


class InfoBar(Static):
    def __init__(
        self,
        content="",
        *,
        expand=False,
        shrink=False,
        markup=True,
        name=None,
        id=None,
        classes=None,
        disabled=False,
    ):
        super().__init__(
            content,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.info = str()

    @on(Resize)
    def _resize_content(self):
        if self.info:
            self.show_info(self.info)
        else:
            self.clear()

    def show_info(self, info: str) -> None:
        self.info = info
        # Calculate the amount of dashes before and after the message
        # to keep the message centered and at least three dashes and a
        # space left and right (4 chars * 2 = 8).
        max_size = self.content_size.width - 8
        if len(info) > max_size:
            info = info[0:max_size]
        filler_count = max_size - len(info)
        if filler_count < 0:
            filler_count = 0
        self.content = (
            "─" * (int(filler_count / 2))
            + "─── "
            + info
            + " ───"
            + "─" * (filler_count - int(filler_count / 2))
        )

    def clear(self):
        self.info = ""
        self.content = "─" * self.content_size.width
