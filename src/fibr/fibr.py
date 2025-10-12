from enum import StrEnum
import logging
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer
from textual.binding import Binding
from textual import events

from fibr.panel import Panel

log = logging.getLogger("main")


def to_selector(id: str) -> str:
    return "#" + id


class PanelID(StrEnum):
    LEFT = "left"
    RIGHT = "right"


class FibrApp(App):
    BINDINGS = [
        # Binding("f1", "help", "Help", key_display="1"),
        # Binding("f2", "menu", "Menu", key_display="2"),
        # Binding("f3", "view", "View", key_display="3"),
        # Binding("f4", "edit", "Edit", key_display="4"),
        # Binding("f5", "copy", "Copy", key_display="5"),
        # Binding(
        #     "f6",
        #     "move",
        #     "RenMov",
        #     key_display="6",
        #     tooltip="      F6 move\nShift+F6 rename",
        # ),
        # Binding("shift+f6", "rename", "RenMov", show=False),
        # Binding("f7", "mkdir", "Mkdir", key_display="7"),
        # Binding("f8", "delete", "Delete", key_display="8"),
        # Binding("f9", "pulldown_menu", "PullDn ", key_display="9"),
        Binding("f10", "quit", "Quit", key_display="10"),
        Binding("ctrl+r", "reload_panel", show=False),
    ]
    COMMAND_PALETTE_BINDING = "ctrl+y"
    CSS_PATH = ["fibr.tcss", "panel/panel.tcss"]

    def __init__(
        self, driver_class=None, css_path=None, watch_css=False, ansi_color=False
    ):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.starting_directory = Path.cwd().resolve()
        self.active_panel = PanelID.LEFT

    def action_help(self) -> None:
        pass

    def action_menu(self) -> None:
        pass

    def action_view(self) -> None:
        pass

    def action_edit(self) -> None:
        pass

    def action_copy(self) -> None:
        pass

    def action_move(self) -> None:
        pass

    def action_rename(self) -> None:
        pass

    def action_mkdir(self) -> None:
        pass

    def action_delete(self) -> None:
        pass

    def action_pulldown_menu(self) -> None:
        pass

    def action_reload_panel(self) -> None:
        panel = self.query_one(to_selector(self.active_panel), Panel)
        panel.reload(use_cache=False)

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Panel(id=PanelID.LEFT, directory=self.starting_directory),
            Panel(id=PanelID.RIGHT, directory=self.starting_directory),
        )
        yield Footer(compact=True, show_command_palette=False)
