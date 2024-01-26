from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal, Optional, Sequence

TYPE_ADRStyle = Literal["MADR2", "MADR3", "nygard"]


@dataclass
class ADRDocument:
    file_path: str
    title: Optional[str] = None
    date: Optional[date] = None
    status: Optional[str] = None
    statuses: Sequence[str] = tuple()
    deciders: Optional[str] = None
    consulted: Optional[str] = None
    informed: Optional[str] = None


class ADRParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(file_path: Path, base_path: Path) -> ADRDocument: ...
