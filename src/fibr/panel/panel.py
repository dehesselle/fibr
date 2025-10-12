from pathlib import Path

from textual.widgets import DataTable, Rule, Input
from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual import on

from fibr.filesystem import Filesystem
from .searchbar import SearchBar


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
        directory: Path,
    ):
        super().__init__(
            *children,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            markup=markup,
        )
        self.directory = directory
        self.fs = Filesystem()

    def compose(self) -> ComposeResult:
        yield DataTable(id=self.id)
        yield Rule()
        yield SearchBar("something here", compact=True, disabled=True)

    @on(SearchBar.Changed)
    def search_and_select(self, event: Input.Changed):
        if not event.input.disabled:
            rowid = self.fs.search.next(self.directory.as_posix(), event.value)
            table = self.query_one(DataTable)
            if rowid:
                table.move_cursor(row=table.get_row_index(str(rowid)))
            else:
                table.add_row(("foo", "bar", "baz"))

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column("Name", width=24)
        table.add_column("Size", width=7)
        table.add_column("Modify time", width=12)

        for row in self.fs.get(self.directory):
            table.add_row(*row[1:], key=str(row[0]))

        table.cursor_type = "row"
        table.cell_padding = 0

    def activate_search(self, character: str):
        search_bar = self.query_one(SearchBar)
        if search_bar.disabled:
            search_bar.disabled = False
            search_bar.value = character
            search_bar.focus()

    def on_search_bar_next(self, message: SearchBar.Next) -> None:
        rowid = self.fs.search.next()
        if rowid:
            table = self.query_one(DataTable)
            table.move_cursor(row=table.get_row_index(str(rowid)))

    def on_search_bar_previous(self, message: SearchBar.Next) -> None:
        rowid = self.fs.search.previous()
        if rowid:
            table = self.query_one(DataTable)
            table.move_cursor(row=table.get_row_index(str(rowid)))
