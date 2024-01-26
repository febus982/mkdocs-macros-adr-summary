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
