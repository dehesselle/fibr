# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path

from textual.app import App
from textual.reactive import var

from fibr.filebrowser import FileBrowser
from fibr.about import AboutDialog

log = logging.getLogger("app")


class FibrApp(App):
    CSS_PATH = ["filebrowser/filebrowser.tcss", "about/about.tcss"]
    SCREENS = {"file_browser": FileBrowser, "about_dialog": AboutDialog}

    starting_directory = var(Path.cwd())

    def on_mount(self) -> None:
        fb: FileBrowser = self.get_screen("file_browser")
        fb.starting_directory = self.starting_directory
        self.push_screen("file_browser")
