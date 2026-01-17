from textual.widget import Widget
import subprocess
from fibr.util.platform import is_windows, is_linux, is_macos
import logging
from pathlib import Path

log = logging.getLogger("fb")


class ExternalCommand(Widget):
    def __init__(self, args: list[str], directory: Path | None = None):
        super().__init__()
        self.args = args
        self.directory = directory

    @property
    def prepared_args(self) -> str:
        if is_linux():
            args = self.args
        elif is_macos():
            args = self.args
        elif is_windows():
            if self.args[0] in ["del", "md", "mkdir", "rmdir"]:
                args = ["cmd.exe", "/C"]
                if self.directory:
                    args.append(f"cd /D {self.directory} && " + " ".join(self.args))
                else:
                    args.append(" ".join(self.args))
            else:
                args = self.args

        log.debug(args)
        return args

    def execute(self) -> None:
        with self.app.suspend():
            try:
                cp = subprocess.run(self.prepared_args)
                if cp.returncode:
                    raise OSError()
            except (FileNotFoundError, OSError):
                self.app.notify(
                    # show unprepared commands here, because that's
                    # what the user entered
                    f"failed to run {self.args[0]}",
                    title=f"error",
                    severity="error",
                    timeout=5,
                )
