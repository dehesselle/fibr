from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Footer
from textual.binding import Binding
from textual import events

from .panel import Panel


class FibrApp(App):
    BINDINGS = [
        Binding("f1", "help", "Help", key_display="1"),
        Binding("f2", "menu", " ", key_display=" "),
        Binding("f3", "view", "View", key_display="3"),
        Binding("f4", "edit", "Edit", key_display="4"),
        Binding("f5", "copy", "Copy", key_display="5"),
        Binding(
            "f6",
            "move",
            "RenMov",
            key_display="6",
            tooltip="      F6 move\nShift+F6 rename",
        ),
        Binding("shift+f6", "rename", "RenMov", show=False),
        Binding("f7", "mkdir", "Mkdir", key_display="7"),
        Binding("f8", "delete", "Delete", key_display="8"),
        Binding("f9", "pulldown_menu", " ", key_display=" "),
        Binding("f10", "quit", "Quit", key_display="10"),
    ]
    CSS_PATH = "fibr.tcss"

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

    def compose(self) -> ComposeResult:
        yield Panel(id="left", starting_dir=self.starting_dir)
        yield Footer(compact=True, show_command_palette=False)

    def on_key(self, event: events.Key):
        if event.character:
            panel = self.query_one("#left", Panel)
            panel.find_as_you_type()

    def set_starting_directory(self, starting_dir: Path):
        self.starting_dir = starting_dir
