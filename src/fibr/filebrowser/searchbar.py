# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from textual.widgets import Input
from textual.binding import Binding
from textual.message import Message
from textual import on


class SearchBar(Input):
    BINDINGS = [
        Binding("escape", "cancel"),
        Binding("tab", "next"),
        Binding("shift+tab", "previous"),
    ]

    def __init__(
        self,
        value=None,
        placeholder="",
        highlighter=None,
        password=False,
        *,
        restrict=None,
        type="text",
        max_length=0,
        suggester=None,
        validators=None,
        validate_on=None,
        valid_empty=False,
        select_on_focus=False,
        name=None,
        id=None,
        classes=None,
        disabled=True,
        tooltip=None,
        compact=True,
    ):
        super().__init__(
            value,
            placeholder,
            highlighter,
            password,
            restrict=restrict,
            type=type,
            max_length=max_length,
            suggester=suggester,
            validators=validators,
            validate_on=validate_on,
            valid_empty=valid_empty,
            select_on_focus=select_on_focus,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            tooltip=tooltip,
            compact=compact,
        )

    class Next(Message):
        pass

    class Previous(Message):
        pass

    class Cancelled(Message):
        pass

    def action_cancel(self):
        self.disabled = True
        self.can_focus = False
        self.post_message(self.Cancelled())

    @on(Input.Submitted)
    def _disable(self):
        self.disabled = True
        self.can_focus = False

    def action_next(self):
        self.post_message(self.Next())

    def action_previous(self):
        self.post_message(self.Previous())
