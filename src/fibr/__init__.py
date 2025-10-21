import argparse
import logging
from pathlib import Path

import fibr.config as config
import fibr.util as util
from .fibr import FibrApp

log = logging.getLogger("main")


def main() -> None:
    parser = argparse.ArgumentParser(description="file browser")
    parser.add_argument(
        "starting_dir",
        type=Path,
        help="starting directory",
        default=".",
        nargs="?",
    )
    parser.add_argument("--version", action="version", version=f"fibr {util.version}")
    args = parser.parse_args()

    util.setup_logging("fibr.log")
    log.info("begin")
    config.load()

    app = FibrApp()
    app.starting_directory = args.starting_dir
    app.run()

    config.save()
    log.info("end")
