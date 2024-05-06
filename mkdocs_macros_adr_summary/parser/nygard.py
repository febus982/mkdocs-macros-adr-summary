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
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .base import BaseParser
from .types import TYPE_AST


class NygardParser(BaseParser):
    @classmethod
    def _get_metadata_and_ast(cls, file: str) -> Tuple[Dict[str, Any], TYPE_AST]:
        md_ast = cls.parser.parse(file)
        return {}, md_ast

    @classmethod
    def _get_date(cls, metadata: dict, ast: TYPE_AST) -> Optional[date]:
        title_index = cls._get_title_index(ast)
        if title_index is None:
            return None

        try:
            block = ast[0][title_index + 2]
        except IndexError:
            return None

        if not block.get("type") == "paragraph":
            return None

        raw_text = cls.renderer.paragraph(block, ast[1]).strip()
        try:
            return datetime.strptime(raw_text, "Date: %Y-%m-%d").date()
        except ValueError:
            return None

    @classmethod
    def _get_statuses(cls, metadata: dict, ast: TYPE_AST) -> Sequence[str]:
        statuses: List[str] = []

        # Find status header
        h2_list = [
            i
            for i, x in enumerate(ast[0])
            if x.get("type") == "heading"
            and x.get("attrs", {}).get("level") == 2
            and cls.renderer.paragraph(x, ast[1]).strip() == "Status"
        ]
        if len(h2_list) != 1:
            return tuple(statuses)

        i = h2_list[0] + 1
        while i < len(ast[0]):
            block = ast[0][i]

            if block.get("type") == "paragraph":
                statuses.append(cls.renderer.paragraph(block, ast[1]).strip())
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
