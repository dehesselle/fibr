from textual.widgets import DataTable


class FileList(DataTable):
    def on_mount(self):
        self.add_column("Name", width=20, key="name")
        self.add_column("Size", width=7, key="size")
        self.add_column("Modify time", width=12, key="modify")
        self.cursor_type = "row"
        self.cell_padding = 1
        super().on_mount()

    @property
    def dynamic_name_column_width(self) -> int:
        return self.size.width - (
            self.columns["size"].width + self.columns["modify"].width + 5
        )

    def _on_resize(self, _):
        super()._on_resize(_)
        self.columns["name"].width = self.dynamic_name_column_width
        self.refresh()
