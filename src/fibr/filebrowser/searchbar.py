# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from textual.widgets import Input
from textual.binding import Binding
from textual.message import Message
from textual import on


class SearchBar(Input):
    class Cancelled(Message):
        pass

    class Next(Message):
        pass

    class Previous(Message):
        pass

    BINDINGS = [
        Binding("escape", "cancel"),
        Binding("tab", "next"),
        Binding("shift+tab", "previous"),
    ]

    def action_cancel(self):
        self.disabled = True
        self.can_focus = False
        self.post_message(self.Cancelled())

    def action_next(self):
        self.post_message(self.Next())

    def action_previous(self):
        self.post_message(self.Previous())

    @on(Input.Submitted)
    def _disable(self):
        self.disabled = True
        self.can_focus = False

    def on_mount(self):
        self.compact = True
        self.disabled = True
        self.select_on_focus = False
