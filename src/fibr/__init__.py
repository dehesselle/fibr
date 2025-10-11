import argparse
from pathlib import Path

from .fibr import FibrApp

try:
    from fibr._version import version
except ImportError:
    version = "0.0.0"


def main() -> None:
    parser = argparse.ArgumentParser(description="file browser")
    parser.add_argument(
        "starting_dir",
        type=Path,
        help="starting directory",
        default=".",
        nargs="?",
    )
    parser.add_argument("--version", action="version", version=f"fibr {version}")
    args = parser.parse_args()

    app = FibrApp()
    app.starting_directory = args.starting_dir
    app.run()
