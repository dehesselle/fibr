from textual.binding import Binding
from textual.message import Message
from textual.widgets import DataTable


class FileList(DataTable):
    BINDINGS = [
        Binding("enter", "execute"),
        Binding("home", "scroll_top"),
        Binding("end", "scroll_bottom"),
    ]

    class Executed(Message):
        def __init__(self, value: str):
            self.value = value
            super().__init__()

    def on_mount(self):
        self.add_column("Name", width=20, key="name")
        self.add_column("Size", width=7, key="size")
        self.add_column("Modify time", width=12, key="modify")
        self.cursor_type = "row"
        self.cell_padding = 1
        super().on_mount()

    @property
    def dynamic_name_column_width(self) -> int:
        return self.size.width - (
            self.columns["size"].width + self.columns["modify"].width + 6
        )

    def _on_resize(self, _):
        super()._on_resize(_)
        self.columns["name"].width = self.dynamic_name_column_width
        self.refresh()

    def action_execute(self):
        name = self.get_cell_at((self.cursor_row, 0))
        self.post_message(self.Executed(name))
