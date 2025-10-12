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
        self.cursor_row_before_search = 0

    def compose(self) -> ComposeResult:
        yield DataTable(id=self.id)
        yield Rule()
        yield SearchBar("something here", compact=True, disabled=True)

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column("Name", width=24)
        table.add_column("Size", width=7)
        table.add_column("Modify time", width=12)
        table.cursor_type = "row"
        table.cell_padding = 0
        self.reload()

    def reload(self):
        table = self.query_one(DataTable)
        table.clear()
        for row in self.fs.get(self.directory, reload=True):
            table.add_row(*row[1:], key=str(row[0]))

    def start_search(self, character: str):
        table = self.query_one(DataTable)
        self.cursor_row_before_search = table.cursor_row
        search_bar = self.query_one(SearchBar)
        if search_bar.disabled:
            search_bar.disabled = False
            search_bar.value = character
            search_bar.focus()

    @on(SearchBar.Changed)
    def _move_cursor_to_first_matchsearch_and_select(self, event: SearchBar.Changed):
        if not event.input.disabled:
            rowid = self.fs.search.next(self.directory.as_posix(), event.value)
            table = self.query_one(DataTable)
            if rowid:
                table.move_cursor(row=table.get_row_index(str(rowid)))

    @on(SearchBar.Next)
    def _move_cursor_to_next_match(self) -> None:
        rowid = self.fs.search.next()
        if rowid:
            table = self.query_one(DataTable)
            table.move_cursor(row=table.get_row_index(str(rowid)))

    @on(SearchBar.Previous)
    def _move_cursor_to_previous_match(self) -> None:
        rowid = self.fs.search.previous()
        if rowid:
            table = self.query_one(DataTable)
            table.move_cursor(row=table.get_row_index(str(rowid)))

    @on(SearchBar.Cancelled)
    def cancel_search(self):
        table = self.query_one(DataTable)
        table.move_cursor(row=self.cursor_row_before_search)
