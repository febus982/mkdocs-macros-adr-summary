#  Copyright (c) 2024 Federico Busetti <729029+febus982@users.noreply.github.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
from datetime import date, datetime
from typing import Any, Dict, Optional, Sequence, Tuple

from .madr3 import BaseParser
from .types import TYPE_AST


class MADR2Parser(BaseParser):
    @classmethod
    def _get_metadata_and_ast(cls, file: str) -> Tuple[Dict[str, Any], TYPE_AST]:
        if file == "":
            raise LookupError("Cannot parse an empty file")
        md_ast = cls.parser.parse(file)

        return cls._get_metadata_from_ast(md_ast), md_ast

    @classmethod
    def _extract_metadata_as_md_string(cls, ast: TYPE_AST) -> Optional[str]:
        title_index = cls._get_title_index(ast)
        content_index = cls._get_first_h2_index(ast)
        if title_index is None or content_index is None:
            raise LookupError(
                "Malformed document: Could not find"
                " headings surrounding metadata section"
            )

        try:
            metadata_list = next(
                x for x in ast[0][title_index:content_index] if x.get("type") == "list"
            )
        except StopIteration:
            # No metadata in the document
            return None

        return cls.renderer.list(metadata_list, ast[1])

    @classmethod
    def _get_metadata_from_ast(cls, ast: TYPE_AST) -> Dict[str, str]:
        metadata: Dict[str, str] = {}
        rendered_metadata = cls._extract_metadata_as_md_string(ast)

        if rendered_metadata is None:
            return metadata

        for item in rendered_metadata.split("\n"):
            if item.startswith("* Status: "):
                metadata["status"] = item[len("* Status: ") :]
            if item.startswith("* Deciders: "):
                metadata["deciders"] = item[len("* Deciders: ") :]
            if item.startswith("* Date: "):
                metadata["date"] = item[len("* Date: ") :]

        return metadata

    @classmethod
    def _get_date(cls, metadata: dict, ast: TYPE_AST) -> Optional[date]:
        if metadata.get("date"):
            return datetime.strptime(metadata["date"], "%Y-%m-%d").date()
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
