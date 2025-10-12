from importlib.resources import read_text
import logging
from sqlite3 import Connection
from typing import List

log = logging.getLogger("fs")

SQL_SEARCH_FILENAME_LIKE = read_text("fibr.filesystem", "search_filename_like.sql")


class Search:
    def __init__(self, db: Connection):
        self.db = db
        self.results = list()
        self.index = -1

    def _db_search_files(
        self, directory: str, filename: str, is_word: bool
    ) -> List[int]:
        if not is_word:
            filename += "%"
        cursor = self.db.execute(
            SQL_SEARCH_FILENAME_LIKE,
            [directory, filename],
        )
        rows = cursor.fetchall()
        log.debug(f"found {len(rows)} rows")

        if len(rows):
            return [row[0] for row in rows]
        else:
            return list()

    def next(
        self, directory: str = None, filename: str = None, is_word: bool = False
    ) -> int:
        if directory:
            self.results = self._db_search_files(directory, filename, is_word)
            self.index = -1

        if len(self.results):
            self.index += 1
            if not self.index < len(self.results):
                self.index = 0

            return self.results[self.index]
        else:
            return 0

    def previous(
        self, directory: str = None, filename: str = None, is_word: bool = False
    ) -> int:
        if directory:
            self.results = self._db_search_files(directory, filename, is_word)
            self.index = -1

        if len(self.results):
            self.index -= 1
            if not self.index > -1:
                self.index = len(self.results) - 1

            return self.results[self.index]
        else:
            return 0
