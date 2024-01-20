from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Literal

ADRStyle = Literal["nygard"]


class ADRFormat(Enum):
    nygard = 1


@dataclass
class ADRDocument:
    filename: str


class ADRParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(file_path: Path) -> ADRDocument:
        ...
