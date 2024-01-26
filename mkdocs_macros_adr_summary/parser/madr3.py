from datetime import date
from typing import Any, Dict, Optional, Sequence, Tuple

from yaml import safe_load
from yaml.scanner import ScannerError

from .base import BaseParser
from .types import TYPE_AST


class MADR3Parser(BaseParser):
    @classmethod
    def _get_metadata_and_ast(cls, file: str) -> Tuple[Dict[str, Any], TYPE_AST]:
        lines = file.splitlines()
        separators = [i for i, x in enumerate(lines) if x == "---"]
        if len(separators) < 2:
            raise LookupError("Metadata section not found in file")

        yaml_file = lines[0 : separators[1] :]
        try:
            metadata: Optional[Dict[str, str]] = safe_load("\n".join(yaml_file))
        except ScannerError:
            raise LookupError("Cannot parse metadata section")

        md_file = lines[separators[1] + 1 : :]
        md_ast = cls.parser.parse("\n".join(md_file))

        return metadata or {}, md_ast

    @classmethod
    def _get_date(cls, metadata: dict, ast: TYPE_AST) -> Optional[date]:
        if isinstance(metadata.get("date"), date):
            return metadata["date"]
        else:
            return None

    @classmethod
    def _get_statuses(cls, metadata: dict, ast: TYPE_AST) -> Sequence[str]:
        if metadata.get("status"):
            return (cls._upperfirst(metadata["status"]),)
        else:
            return tuple()

    @classmethod
    def _get_status(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]:
        try:
            return cls._get_statuses(metadata, ast)[0]
        except IndexError:
            return None

    @classmethod
    def _get_deciders(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]:
        return metadata.get("deciders")

    @classmethod
    def _get_consulted(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]:
        return metadata.get("consulted")

    @classmethod
    def _get_informed(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]:
        return metadata.get("informed")
