from textual.widgets import DataTable, Rule, Input
from textual.app import ComposeResult
from textual.containers import VerticalGroup

from textual import on

from fibr.filesystem import Filesystem, NotFoundException

from .searchbar import SearchBar

from pathlib import Path


class Panel(VerticalGroup):
    CSS_PATH = "panel.tcss"

    def __init__(
        self,
        *children,
        name=None,
        id=None,
        classes=None,
        disabled=False,
        markup=True,
        starting_dir: Path,
    ):
        super().__init__(
            *children,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            markup=markup,
        )
        self.starting_dir = starting_dir
        self.fs = Filesystem()

    def compose(self) -> ComposeResult:
        yield DataTable(id=self.id)
        yield Rule()
        yield SearchBar("something here", compact=True, disabled=True)

    @on(SearchBar.Changed)
    def search_and_select(self, event: Input.Changed):
        if not event.input.disabled:
            self.select_row(event.value)

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column("Name", width=24)
        table.add_column("Size", width=7)
        table.add_column("Modify time", width=12)

        for row in self.fs.get(self.starting_dir):
            table.add_row(*row[1:], key=str(row[0]))

        table.cursor_type = "row"
        table.cell_padding = 0

    def select_row(self, name):
        table = self.query_one(DataTable)
        try:
            table.move_cursor(
                row=table.get_row_index(self.fs.get_rowid(self.starting_dir, name))
            )
        except NotFoundException as e:
            pass

    def find_as_you_type(self):
        input = self.query_one(Input)
        input.disabled = False
        input.clear()
        input.focus()
