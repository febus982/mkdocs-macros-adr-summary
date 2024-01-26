from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple

from mistune import Markdown, create_markdown
from mistune.renderers.markdown import MarkdownRenderer
from mkdocs_macros import fix_url

from mkdocs_macros_adr_summary.interfaces import ADRDocument, ADRParser

from .exceptions import InvalidFileError
from .types import TYPE_AST


class BaseParser(ADRParser, ABC):
    renderer: MarkdownRenderer = MarkdownRenderer()
    parser: Markdown = create_markdown(
        escape=False,
        renderer=None,
        plugins=["strikethrough", "footnotes", "table", "speedup"],
    )

    @classmethod
    def parse(cls, file_path: Path, base_path: Path) -> ADRDocument:
        with open(file_path, "r") as f:
            file = f.read()
        try:
            metadata, ast = cls._get_metadata_and_ast(file)
        except LookupError as e:
            raise InvalidFileError(file_path) from e

        doc = ADRDocument(
            file_path=fix_url(str(file_path.relative_to(base_path))),
            title=cls._get_title(metadata, ast),
            date=cls._get_date(metadata, ast),
            status=cls._get_status(metadata, ast),
            statuses=cls._get_statuses(metadata, ast),
            deciders=cls._get_deciders(metadata, ast),
            consulted=cls._get_consulted(metadata, ast),
            informed=cls._get_informed(metadata, ast),
        )

        return doc

    @classmethod
    def _get_title(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]:
        h1_list = [
            i
            for i, x in enumerate(ast[0])
            if x.get("type") == "heading" and x.get("attrs", {}).get("level") == 1
        ]
        if len(h1_list) != 1:
            return None

        return cls.renderer.paragraph(ast[0][h1_list[0]], ast[1]).strip()

    @classmethod
    @abstractmethod
    def _get_date(cls, metadata: dict, ast: TYPE_AST) -> Optional[date]: ...

    @classmethod
    @abstractmethod
    def _get_statuses(cls, metadata: dict, ast: TYPE_AST) -> Sequence[str]: ...

    @classmethod
    @abstractmethod
    def _get_status(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]: ...

    @classmethod
    @abstractmethod
    def _get_metadata_and_ast(cls, file: str) -> Tuple[Dict[str, Any], TYPE_AST]: ...

    @classmethod
    @abstractmethod
    def _get_deciders(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]: ...

    @classmethod
    @abstractmethod
    def _get_consulted(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]: ...

    @classmethod
    @abstractmethod
    def _get_informed(cls, metadata: dict, ast: TYPE_AST) -> Optional[str]: ...

    @staticmethod
    def _upperfirst(text: str) -> str:
        return text[0].capitalize() + text[1::] if text[0].islower() else text
