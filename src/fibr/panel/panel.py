import logging
from pathlib import Path

from textual.widgets import DataTable, Rule
from textual.widgets.data_table import RowKey
from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual import events, on

from fibr.filesystem import Filesystem
from .searchbar import SearchBar

log = logging.getLogger("panel")


class Panel(VerticalGroup):
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
        yield SearchBar()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column("Name", width=24, key="name")
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
            search_bar.can_focus = True
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

    def on_key(self, event: events.Key):
        if event.character and event.character.isprintable():
            self.start_search(event.character)

    @on(DataTable.RowHighlighted)
    def _show_highlighted_row_in_search_bar(self, event: DataTable.RowHighlighted):
        self.show_filename_in_search_bar(event.row_key)

    def show_filename_in_search_bar(self, row_key: RowKey | str):
        search_bar = self.query_one(SearchBar)
        # Only use the search bar as an info bar if it's not in use.
        if search_bar.disabled:
            table = self.query_one(DataTable)
            if isinstance(row_key, RowKey):
                search_bar.value = table.get_cell(row_key, "name")
            else:
                search_bar.value = row_key

    @on(SearchBar.Submitted)
    def _show_submitted_search_in_search_bar(self, event: SearchBar.Submitted):
        table = self.query_one(DataTable)
        self.show_filename_in_search_bar(table.get_cell_at((table.cursor_row, 0)))
