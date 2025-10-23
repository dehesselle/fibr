# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path
import re
import subprocess
from typing import List

from rich.text import Text
from textual.widgets.data_table import RowKey, RowDoesNotExist
from textual.app import ComposeResult
from textual.containers import Vertical
from textual import events, on
from textual.binding import Binding
from textual.message import Message
from textual.color import Color

from fibr.filesystem import Filesystem
import fibr.util as util
from .searchbar import SearchBar
from .filelist import FileList
from .infobar import InfoBar


log = logging.getLogger("panel")


class Panel(Vertical):
    class InternalCommandSubmitted(Message):
        def __init__(self, panel_id, command, files: List[Path]):
            super().__init__()
            self.panel_id = panel_id
            self.command = command
            self.files = files

    BINDINGS = [
        Binding("f1", "app.push_screen('about_dialog')", "About"),
        Binding("f3", "view", "View"),
        Binding("f4", "edit", "Edit"),
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
        Binding("f10", "app.quit", "Quit"),
        Binding("ctrl+o", "shell", "Open shell", show=False),
        Binding("ctrl+r", "reload", "Reload", show=False),
        Binding("ctrl+t", "toggle_select", "Select", show=False),
        Binding("insert", "toggle_select", "Select", show=False),
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
        self.selected_rows = list()

    def action_edit(self) -> None:
        object = self.directory / self.fs.get_file_name_by_id(
            int(self.highlighted_row.value)
        )
        if object.is_file():
            self.execute_external_command([util.get_editor(), object])

    def action_reload(self) -> None:
        self.reload(use_cache=False)

    def action_shell(self) -> None:
        self.execute_external_command([util.get_shell()])

    def action_toggle_select(self) -> None:
        table = self.query_one(FileList)
        if self.highlighted_row in self.selected_rows:
            self.selected_rows.remove(self.highlighted_row)
            table.update_cell(
                self.highlighted_row,
                "name",
                self.fs.get_file_name_by_id(int(self.highlighted_row.value)),
            )
        else:
            self.selected_rows.append(self.highlighted_row)
            table.update_cell(
                self.highlighted_row,
                "name",
                Text(
                    self.fs.get_file_name_by_id(int(self.highlighted_row.value)),
                    style=f"default bold on {Color.parse('sienna').hex}",
                ),
            )
        table.move_cursor(row=table.cursor_row + 1)

    def action_view(self) -> None:
        object = self.directory / self.fs.get_file_name_by_id(
            int(self.highlighted_row.value)
        )
        if object.is_file():
            self.execute_external_command([util.get_viewer(), object])

    def compose(self) -> ComposeResult:
        yield FileList(id=self.id)
        yield InfoBar()
        yield SearchBar()

    def execute_external_command(self, args: List[str]) -> None:
        with self.app.suspend():
            cp = subprocess.run(args)
            if cp.returncode:
                self.app.notify(
                    f"failed to run {args[0]}",
                    title=f"error (rc={cp.returncode})",
                    severity="error",
                    timeout=5,
                )

    def reload(self, use_cache: bool = True):
        if self.directory.name == "..":
            parent_name = self.directory.parent.name
        else:
            parent_name = str()

        self.directory = self.directory.resolve()
        table = self.query_one(FileList)
        table.clear()
        for row in self.fs.get_files(self.directory, use_cache=use_cache):
            table.add_row(
                (
                    Text(row[1], style=f"default bold on {Color.parse('sienna').hex}")
                    if RowKey(str(row[0])) in self.selected_rows
                    else row[1]
                ),
                util.bytes_to_str(row[2]),
                util.epoch_to_str(row[3]),
                key=str(row[0]),
            )
        self.border_title = self.directory.name

        if parent_name:
            file_id = self.fs.get_file_id(self.directory, parent_name)
            try:
                table.move_cursor(row=table.get_row_index(str(file_id)))
            except RowDoesNotExist:
                log.error(f"cannot move cursor for file_id={file_id}")

    def show_name_in_search_bar(self, name: RowKey | str):
        search_bar = self.query_one(SearchBar)
        # Only use the search bar as an info bar if it's not in use.
        if search_bar.disabled:
            if isinstance(name, RowKey):
                search_bar.value = self.fs.get_file_name_by_id(int(name.value))
            else:
                search_bar.value = name

    def start_search(self, character: str):
        table = self.query_one(FileList)
        self.cursor_row_before_search = table.cursor_row
        search_bar = self.query_one(SearchBar)
        if search_bar.disabled:
            search_bar.can_focus = True
            search_bar.disabled = False
            search_bar.value = character
            search_bar.focus()

    @on(FileList.Executed)
    def _change_directory(self, event: FileList.Executed):
        target = self.directory / self.fs.get_file_name_by_id(
            int(self.highlighted_row.value)
        )
        log.debug(f"target: {target}")
        if target.is_dir():
            self.selected_rows.clear()
            self.directory = target
            self.reload()

    @on(FileList.RowHighlighted)
    def _show_highlighted_row_in_search_bar(self, event: FileList.RowHighlighted):
        self.highlighted_row = event.row_key
        self.show_name_in_search_bar(self.highlighted_row)

    @on(SearchBar.Cancelled)
    def cancel_search(self):
        table = self.query_one(FileList)
        table.move_cursor(row=self.cursor_row_before_search)

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

    @on(SearchBar.Submitted)
    def _process_search_result(self, event: SearchBar.Submitted):
        log.debug(f"event.value: {event.value}")
        name = self.fs.get_file_name_by_id(int(self.highlighted_row.value))

        # drive letter on windows: change drive
        if re.match(r"^[A-Za-z]\:$", event.value) and util.is_windows():
            directory = Path(event.value + "/")
            if directory.exists():
                self.directory = directory
                self.reload()
            else:
                self.app.notify(
                    f"does not exist: {directory}",
                    title="error",
                    severity="error",
                    timeout=5,
                )
        # colon-nonspace: execute external command
        elif match := re.match(r"^:([^ ].+)", event.value):
            self.execute_external_command(match.group(1).split())
        # colon-space: execute internal command
        elif match := re.match(r"^: ([^ ].+)", event.value):
            self.post_message(
                self.InternalCommandSubmitted(
                    self.id,
                    match.group(1),
                    (
                        [
                            self.directory / self._get_file_by_id(row)
                            for row in self.selected_rows
                        ]
                        if self.selected_rows
                        else [
                            self.directory / self._get_file_by_id(self.highlighted_row)
                        ]
                    ),
                ),
            )
        # directory: enter the directory
        elif (
            name.startswith(event.value)
            and (directory := self.directory / name).is_dir()
        ):
            self.directory = directory
            self.selected_rows.clear()
            self.reload()
        else:
            self.show_name_in_search_bar(name)

    def on_key(self, event: events.Key):
        if (
            event.character
            and event.character.isprintable()
            and not event.character.isspace()
        ):
            self.start_search(event.character)

    def on_mount(self) -> None:
        self.reload()

    def _get_file_by_id(self, row: RowKey) -> str:
        return self.fs.get_file_name_by_id(int(row.value))
