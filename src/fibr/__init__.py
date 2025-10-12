import argparse
import logging
import os
from pathlib import Path

from .fibr import FibrApp

try:
    from fibr._version import version
except ImportError:
    version = "0.0.0"

log = logging.getLogger("main")


def setup_logging(logfile: str) -> None:
    level = os.environ.get("FIBR_LOGLEVEL", "").upper()

    if level:
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)-23s | %(name)-14s | %(funcName)-20s | %(levelname)-8s | %(message)s"
            )
        )

        logging.basicConfig(
            level=level,
            handlers=[
                file_handler,
            ],
        )


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

    setup_logging("fibr.log")

    log.info("begin")
    app = FibrApp()
    app.starting_directory = args.starting_dir.resolve()
    app.run()
    log.info("end")
