from datetime import date, datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .base import BaseParser
from .types import TYPE_AST


class NygardParser(BaseParser):
    @classmethod
    def _get_metadata_and_ast(cls, file: str) -> Tuple[Dict[str, Any], TYPE_AST]:
        md_ast = cls.parser.parse(file)
        return {}, md_ast

    @classmethod
    def _get_date(cls, metadata: dict, document: TYPE_AST) -> Optional[date]:
        h1_list = [
            i
            for i, x in enumerate(document[0])
            if x.get("type") == "heading" and x.get("attrs", {}).get("level") == 1
        ]
        if len(h1_list) != 1:
            return None

        try:
            block = document[0][h1_list[0] + 2]
        except IndexError:
            return None

        if not block.get("type") == "paragraph":
            return None

        raw_text = cls.renderer.paragraph(block, document[1]).strip()
        try:
            return datetime.strptime(raw_text, "Date: %Y-%m-%d").date()
        except ValueError:
            return None

    @classmethod
    def _get_statuses(cls, metadata: dict, document: TYPE_AST) -> Sequence[str]:
        statuses: List[str] = []

        # Find status header
        h2_list = [
            i
            for i, x in enumerate(document[0])
            if x.get("type") == "heading"
            and x.get("attrs", {}).get("level") == 2
            and cls.renderer.paragraph(x, document[1]).strip() == "Status"
        ]
        if len(h2_list) != 1:
            return tuple(statuses)

        i = h2_list[0] + 1
        while i < len(document[0]):
            block = document[0][i]

            if block.get("type") == "paragraph":
                statuses.append(cls.renderer.paragraph(block, document[1]).strip())
                i += 1
            elif block.get("type") == "heading":
                break
            else:
                i += 1
                continue

        return tuple(statuses)

    @classmethod
    def _get_status(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]:
        statuses = cls._get_statuses(metadata, ast)
        return statuses[-1] if statuses else None

    @classmethod
    def _get_deciders(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]:
        return None

    @classmethod
    def _get_consulted(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]:
        return None

    @classmethod
    def _get_informed(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]:
        return None
