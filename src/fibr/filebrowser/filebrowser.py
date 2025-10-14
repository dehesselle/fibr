from enum import StrEnum
from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer

from .panel import Panel


class PanelID(StrEnum):
    LEFT = "left"
    RIGHT = "right"


class FileBrowser(Screen):
    BINDINGS = [
        # Binding("f1", "help", "Help", key_display="1"),
        # Binding("f2", "menu", "Menu", key_display="2"),
        # Binding("f9", "pulldown_menu", "PullDn ", key_display="9"),
        Binding("f10", "app.quit", "Quit", key_display="10"),
    ]

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.starting_directory = Path.cwd()
        self.active_panel = PanelID.LEFT

    def action_help(self) -> None:
        pass

    def action_menu(self) -> None:
        pass

    def action_pulldown_menu(self) -> None:
        pass

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Panel(id=PanelID.LEFT, directory=self.starting_directory),
            Panel(id=PanelID.RIGHT, directory=self.starting_directory),
        )
        yield Footer(compact=True, show_command_palette=False)
