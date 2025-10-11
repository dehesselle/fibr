from textual.widgets import Input
from textual.binding import Binding
from textual.message import Message


class SearchBar(Input):
    BINDINGS = [
        Binding("escape", "disable"),
        Binding("ctrl+n", "next"),
        Binding("ctrl+p", "previous"),
    ]

    class Next(Message):
        pass

    class Previous(Message):
        pass

    def action_disable(self):
        self.disabled = True

    def action_next(self):
        self.post_message(self.Next())

    def action_previous(self):
        self.post_message(self.Previous())

    def on_mount(self):
        self.select_on_focus = False
        return super().on_mount()
