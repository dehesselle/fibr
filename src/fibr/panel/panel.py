from textual.widgets import DataTable, Rule, Input
from textual.app import ComposeResult
from textual.containers import VerticalGroup

from textual import on

from fibr.filesystem import Filesystem

from .searchbar import SearchBar

from pathlib import Path


class Search:
    def __init__(self, filesystem: Filesystem):
        self.fs = filesystem
        self.results = list()
        self.index = -1

    def search_files(self, directory: Path, filename: str):
        self.results = self.fs.get_rowids(directory, filename)
        self.index = -1

    def get_next(self) -> int:
        if len(self.results):
            self.index += 1
            if not self.index < len(self.results):
                self.index = 0

            return self.results[self.index]
        else:
            return 0

    def get_previous(self) -> int:
        if len(self.results):
            self.index -= 1
            if not self.index > -1:
                self.index = len(self.results) - 1

            return self.results[self.index]
        else:
            return 0


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
        self.search = Search(self.fs)

    def compose(self) -> ComposeResult:
        yield DataTable(id=self.id)
        yield Rule()
        yield SearchBar("something here", compact=True, disabled=True)

    @on(SearchBar.Changed)
    def search_and_select(self, event: Input.Changed):
        if not event.input.disabled:
            self.search.search_files(self.directory, event.value)
            rowid = self.search.get_next()
            if rowid:
                table = self.query_one(DataTable)
                table.move_cursor(row=table.get_row_index(str(rowid)))

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
        rowid = self.search.get_next()
        if rowid:
            table = self.query_one(DataTable)
            table.move_cursor(row=table.get_row_index(str(rowid)))

    def on_search_bar_previous(self, message: SearchBar.Next) -> None:
        rowid = self.search.get_previous()
        if rowid:
            table = self.query_one(DataTable)
            table.move_cursor(row=table.get_row_index(str(rowid)))
