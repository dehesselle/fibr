import logging
from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, TextArea

log = logging.getLogger("viewer")


class FileViewer(Screen):
    BINDINGS = [
        Binding("f2", "toggle_wrap", "Un/Wrap", key_display="2"),
        Binding("f3", "app.pop_screen", "Quit", key_display="3"),
        Binding("f10", "app.pop_screen", "Quit", key_display="10"),
    ]

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.text_area = TextArea(read_only=True)

    def compose(self) -> ComposeResult:
        yield self.text_area
        yield Footer(compact=True, show_command_palette=False)

    def read(self, file: Path) -> None:
        try:
            self.text_area.text = file.read_text(encoding="UTF-8")
            return
        except UnicodeDecodeError:
            pass
        try:
            self.text_area.text = file.read_text()
        except UnicodeDecodeError:
            self.text_area.text = f"unable to view/decode file: {file}"

    def action_toggle_wrap(self):
        self.text_area.soft_wrap = not self.text_area.soft_wrap
