from textual.widgets import Input
from textual.binding import Binding


class SearchBar(Input):
    BINDINGS = [Binding("escape", "disable")]

    def action_disable(self):
        self.disabled = True
