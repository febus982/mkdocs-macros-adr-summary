from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Literal, Optional

ADRStyle = Literal["nygard"]


class ADRFormat(Enum):
    nygard = 1


@dataclass
class ADRDocument:
    filename: str
    title: str
    date: Optional[date]
    status: Optional[str]


class ADRParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(file_path: Path) -> ADRDocument:
        ...
