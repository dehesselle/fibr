# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from textual.binding import Binding
from textual.message import Message
from textual.widgets import DataTable
from textual.widgets.data_table import ColumnKey


class FileList(DataTable):
    BINDINGS = [
        Binding("enter", "execute", "Enter directory", show=False),
        Binding("home", "scroll_top", "Cursor top", show=False),
        Binding("end", "scroll_bottom", "Cursor bottom", show=False),
    ]

    class Executed(Message):
        pass

    def on_mount(self):
        self.add_column("Name", width=1, key="name")
        self.add_column("Size", width=7, key="size")
        self.add_column("Modify time", width=12, key="mtime")
        self.cursor_type = "row"
        self.cell_padding = 1
        super().on_mount()

    @property
    def max_name_column_width(self) -> int:

        return self.size.width - (
            self.columns[ColumnKey("size")].width
            + self.columns[ColumnKey("mtime")].width
            + 7
        )

    def _on_resize(self, _):
        super()._on_resize(_)
        self.columns[ColumnKey("name")].width = self.max_name_column_width
        self.refresh()

    def action_execute(self):
        self.post_message(self.Executed())
