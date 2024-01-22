from datetime import date, datetime
from pathlib import Path
from typing import Optional, Union, Tuple

from marko import parse
from marko.block import Document, Heading, Paragraph
from marko.inline import RawText

from mkdocs_macros_adr_summary.interfaces import ADRDocument, ADRParser


class NygardParser(ADRParser):
    @classmethod
    def parse(cls, file_path: Path) -> ADRDocument:
        with open(file_path, "r") as f:
            md_file = parse(f.read())

        doc = ADRDocument(
            filename=str(file_path),
            title=cls._get_title(md_file) or "==INVALID_TITLE==",
            date=cls._get_datetime(md_file),
            statuses=cls._get_statuses(md_file) or ("==INVALID_STATUS==",),
        )
        return doc

    @classmethod
    def _get_title(cls, document: Document) -> Optional[str]:
        try:
            block = document.children[0]
            if not isinstance(block, Heading) or block.level != 1:
                raise ValueError("Invalid title block.")
            return cls._get_raw_content(block)
        except (IndexError, ValueError):
            return None

    @classmethod
    def _get_datetime(cls, document: Document) -> Optional[date]:
        try:
            block = document.children[2]
            if not isinstance(block, Paragraph):
                raise ValueError("Invalid date block.")
            raw_text = cls._get_raw_content(block)
            return datetime.strptime(raw_text, "Date: %Y-%m-%d").date()  # type: ignore
        except (IndexError, ValueError):
            return None

    @classmethod
    def _get_statuses(cls, document: Document) -> Optional[Tuple[str]]:
        statuses = []
        try:
            block = document.children[6]
            if not isinstance(block, Paragraph):
                raise ValueError("Invalid status block.")
            statuses.append(cls._get_raw_content(block))
        except (IndexError, ValueError):
            return None

        return tuple(statuses)

    @classmethod
    def _get_raw_content(cls, block: Union[Paragraph, Heading]) -> Optional[str]:
        return [x.children for x in block.children if isinstance(x, RawText)][0]
