from textual.widgets import Input
from textual.binding import Binding
from textual.message import Message
from textual import on


class SearchBar(Input):
    BINDINGS = [
        Binding("escape", "cancel"),
        Binding("ctrl+n", "next"),
        Binding("ctrl+p", "previous"),
    ]

    class Next(Message):
        pass

    class Previous(Message):
        pass

    class Cancelled(Message):
        pass

    def action_cancel(self):
        self.disabled = True
        self.post_message(self.Cancelled())

    @on(Input.Submitted)
    def _disable(self):
        self.disabled = True

    def action_next(self):
        self.post_message(self.Next())

    def action_previous(self):
        self.post_message(self.Previous())

    def on_mount(self):
        self.select_on_focus = False
        return super().on_mount()
