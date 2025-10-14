import logging
from os import system
from pathlib import Path

from textual.widgets import Rule
from textual.widgets.data_table import RowKey
from textual.app import ComposeResult
from textual.containers import Vertical
from textual import events, on
from textual.binding import Binding

from fibr.filesystem import Filesystem
import fibr.util as util
from .searchbar import SearchBar
from .filelist import FileList


log = logging.getLogger("panel")


class Panel(Vertical):
    BINDINGS = [
        # Binding("f3", "view", "View", key_display="3"),
        Binding("f4", "edit", "Edit", key_display="4"),
        # Binding("f5", "copy", "Copy", key_display="5"),
        # Binding(
        #     "f6",
        #     "move",
        #     "RenMov",
        #     key_display="6",
        #     tooltip="      F6 move\nShift+F6 rename",
        # ),
        # Binding("shift+f6", "rename", "RenMov", show=False),
        # Binding("f7", "mkdir", "Mkdir", key_display="7"),
        # Binding("f8", "delete", "Delete", key_display="8"),
        Binding("ctrl+r", "reload", show=False),
    ]

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
        self.highlighted_row = RowKey()

    def compose(self) -> ComposeResult:
        yield FileList(id=self.id)
        yield Rule()
        yield SearchBar()

    def on_mount(self) -> None:
        self.reload()

    def reload(self, use_cache: bool = True):
        table = self.query_one(FileList)
        table.clear()
        self.directory = self.directory.resolve()
        for row in self.fs.get(self.directory, use_cache=use_cache):
            table.add_row(
                row[1],
                util.bytes_to_str(row[2]),
                util.epoch_to_str(row[3]),
                key=str(row[0]),
            )

    def start_search(self, character: str):
        table = self.query_one(FileList)
        self.cursor_row_before_search = table.cursor_row
        search_bar = self.query_one(SearchBar)
        if search_bar.disabled:
            search_bar.can_focus = True
            search_bar.disabled = False
            search_bar.value = character
            search_bar.focus()

    @on(SearchBar.Changed)
    def _move_cursor_to_first_match(self, event: SearchBar.Changed):
        if not event.input.disabled:
            rowid = self.fs.search.next(str(self.directory), event.value)
            table = self.query_one(FileList)
            if rowid:
                table.move_cursor(row=table.get_row_index(str(rowid)))

    @on(SearchBar.Next)
    def _move_cursor_to_next_match(self) -> None:
        rowid = self.fs.search.next()
        if rowid:
            table = self.query_one(FileList)
            table.move_cursor(row=table.get_row_index(str(rowid)))

    @on(SearchBar.Previous)
    def _move_cursor_to_previous_match(self) -> None:
        rowid = self.fs.search.previous()
        if rowid:
            table = self.query_one(FileList)
            table.move_cursor(row=table.get_row_index(str(rowid)))

    @on(SearchBar.Cancelled)
    def cancel_search(self):
        table = self.query_one(FileList)
        table.move_cursor(row=self.cursor_row_before_search)

    def on_key(self, event: events.Key):
        if event.character and event.character.isprintable():
            self.start_search(event.character)

    @on(FileList.RowHighlighted)
    def _show_highlighted_row_in_search_bar(self, event: FileList.RowHighlighted):
        self.highlighted_row = event.row_key
        self.show_name_in_search_bar(self.highlighted_row)

    def show_name_in_search_bar(self, row_key: RowKey | str):
        search_bar = self.query_one(SearchBar)
        # Only use the search bar as an info bar if it's not in use.
        if search_bar.disabled:
            table = self.query_one(FileList)
            if isinstance(row_key, RowKey):
                search_bar.value = table.get_cell(row_key, "name")
            else:
                search_bar.value = row_key

    @on(SearchBar.Submitted)
    def _process_search_result(self, event: SearchBar.Submitted):
        table = self.query_one(FileList)
        name = table.get_cell_at((table.cursor_row, 0))
        self.show_name_in_search_bar(name)

        # if it's a directory: enter the directory
        if (directory := self.directory / name).is_dir():
            self.directory = directory
            self.reload()

    @on(FileList.Executed)
    def _change_directory(self, event: FileList.Executed):
        target = self.directory / event.value
        log.debug(f"target: {target}")
        if target.is_dir():
            self.directory = target
            self.reload()

    def action_edit(self) -> None:
        with self.app.suspend():
            table = self.query_one(FileList)
            object = Path(table.get_cell(self.highlighted_row, "name"))
            if object.is_file():
                editor = util.get_editor()
                rc = system(f"{editor} {object}")
                if rc:
                    self.app.notify(
                        f"failed to call editor {editor}",
                        title="error",
                        severity="error",
                        timeout=5,
                    )

    def action_reload(self) -> None:
        self.reload(use_cache=False)
