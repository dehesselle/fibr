from enum import StrEnum
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer

from .panel import Panel


class PanelID(StrEnum):
    LEFT = "left"
    RIGHT = "right"


class FileBrowser(Screen):
    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.starting_directory = Path.cwd()
        self.active_panel = PanelID.LEFT

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Panel(id=PanelID.LEFT, directory=self.starting_directory),
            Panel(id=PanelID.RIGHT, directory=self.starting_directory),
        )
        yield Footer(compact=True, show_command_palette=False)
