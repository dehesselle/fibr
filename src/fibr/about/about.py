from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import TextArea, Footer

import fibr.util as util


# pyfiglet -f cricket fibr
ABOUT_TEXT = """
      ___ __ __
    .'  _|__|  |--.----.          fibr [faɪbə]
    |   _|  |  _  |   _|
    |__| |__|_____|__|       dual-pane file browser


  First line of text here! Max line size ----------->|



  Last line of text here! Max line size ------------>|

  (c) 2025 René de Hesselle.
  Licensed under [TBD].
"""


class AboutDialog(ModalScreen):
    BINDINGS = [Binding("escape", "app.pop_screen", "Cancel", show=True)]

    def compose(self) -> ComposeResult:
        yield TextArea(read_only=True, show_cursor=False)
        yield Footer()

    def on_mount(self):
        ta = self.query_one(TextArea)
        ta.text = ABOUT_TEXT
        ta.border_title = "v" + util.version
