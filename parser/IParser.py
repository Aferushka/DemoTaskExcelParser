from abc import ABC, abstractmethod
from typing import List
from collections import namedtuple


class IParser(ABC):
    def __init__(self, filename: str, sheetname: str):
        self.filename = filename
        self.sheetname = sheetname

    @abstractmethod
    def go_parse(self) -> List[namedtuple]:
        ...
