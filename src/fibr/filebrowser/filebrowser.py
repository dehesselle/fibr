# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from enum import StrEnum, auto
import logging
from pathlib import Path
import shutil

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer
from textual import on

from .panel import Panel

log = logging.getLogger("fb")


class PanelID(StrEnum):
    ONE = auto()
    TWO = auto()

    @classmethod
    def get_other(cls, id: str):
        match id:
            case cls.ONE:
                return cls.TWO
            case cls.TWO:
                return cls.ONE


class FileBrowser(Screen):
    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.starting_directory = Path.cwd()

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Panel(id=PanelID.ONE, directory=self.starting_directory),
            Panel(id=PanelID.TWO, directory=self.starting_directory),
        )
        yield Footer(compact=True, show_command_palette=False)

    @on(Panel.InternalCommandSubmitted)
    def _execute_command(self, event: Panel.InternalCommandSubmitted):
        target_directory = self.query_one(
            "#" + PanelID.get_other(event.panel_id), Panel
        ).directory
        match event.command:
            case "cp":
                for file in event.files:
                    if file.is_dir():
                        shutil.copytree(file, target_directory / file.name)
                    elif file.is_file():
                        shutil.copy(file, target_directory / file.name)
                    else:
                        log.error(
                            f"not copying, neither file or directory: {file.name}"
                        )
            case "mv":
                for file in event.files:
                    if file.is_dir() or file.is_file():
                        shutil.move(file, target_directory / file.name)
                    else:
                        log.error(f"not moving, neither file or directory: {file.name}")
            case "rm":
                for file in event.files:
                    if file.is_dir():
                        shutil.rmtree(file)
                    elif file.is_file():
                        file.unlink()
                    else:
                        log.error(
                            f"not deleting, neither file or directory: {file.name}"
                        )
            case _:
                log.error(f"unknown command: {event.command}")
