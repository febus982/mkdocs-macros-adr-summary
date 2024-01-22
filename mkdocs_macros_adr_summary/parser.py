from datetime import date, datetime
from pathlib import Path
from typing import List, Optional, Tuple

from mistune import BlockState, Markdown, create_markdown
from mistune.renderers.markdown import MarkdownRenderer

from mkdocs_macros_adr_summary.interfaces import ADRDocument, ADRParser

AST_TYPE = Tuple[List, BlockState]


class NygardParser(ADRParser):
    renderer = MarkdownRenderer()
    parser: Markdown = create_markdown(
        escape=False,
        renderer=None,
        plugins=["strikethrough", "footnotes", "table", "speedup"],
    )

    @classmethod
    def parse(cls, file_path: Path) -> ADRDocument:
        with open(file_path, "r") as f:
            md_ast = cls.parser.parse(f.read())

        doc = ADRDocument(
            filename=str(file_path),
            title=cls._get_title(md_ast) or "==INVALID_TITLE==",
            date=cls._get_datetime(md_ast),
            statuses=cls._get_statuses(md_ast) or ("==INVALID_STATUS==",),
        )
        return doc

    @classmethod
    def _get_title(cls, document: AST_TYPE) -> Optional[str]:
        try:
            block = document[0][0]
        except IndexError:
            return None

        if (
            not block.get("type") == "heading"
            or block.get("attrs", {}).get("level") != 1
        ):
            return None

        return cls.renderer.paragraph(block, document[1]).strip()

    @classmethod
    def _get_datetime(cls, document: AST_TYPE) -> Optional[date]:
        try:
            block = document[0][2]
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
    def _get_statuses(cls, document: AST_TYPE) -> Optional[Tuple[str, ...]]:
        statuses: List[str] = []

        try:
            block = document[0][6]
        except IndexError:
            return None

        if not block.get("type") == "paragraph":
            return None

        statuses.append(cls.renderer.paragraph(block, document[1]).strip())

        return tuple(statuses)
