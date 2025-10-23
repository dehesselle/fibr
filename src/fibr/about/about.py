# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from importlib.resources import read_text

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import TextArea, Footer

import fibr.util as util

# logo: pyfiglet -f cricket fibr
ABOUT_TEXT = read_text("fibr.about", "about.txt")


class AboutDialog(ModalScreen):
    BINDINGS = [Binding("escape", "app.pop_screen", "Cancel", show=True)]

    def compose(self) -> ComposeResult:
        yield TextArea(read_only=True, show_cursor=False)
        yield Footer()

    def on_mount(self):
        ta = self.query_one(TextArea)
        ta.text = ABOUT_TEXT
        ta.border_title = "v" + util.version
