import logging
import os


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
