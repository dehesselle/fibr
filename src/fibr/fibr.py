# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path

from textual.app import App

from fibr.filebrowser import FileBrowser
from fibr.about import AboutDialog

log = logging.getLogger("app")


class FibrApp(App):
    CSS_PATH = ["filebrowser/filebrowser.tcss", "about/about.tcss"]
    SCREENS = {"file_browser": FileBrowser, "about_dialog": AboutDialog}

    def __init__(
        self, driver_class=None, css_path=None, watch_css=False, ansi_color=False
    ):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.starting_directory = Path.cwd()

    def on_mount(self) -> None:
        self.push_screen("file_browser")
