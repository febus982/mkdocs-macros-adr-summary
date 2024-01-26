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

import os
import re
from pathlib import Path
from typing import Optional

from mkdocs_macros.plugin import MacrosPlugin

from .factory import get_parser
from .interfaces import TYPE_ADRStyle
from .renderer import Jinja2Renderer

ADR_REGEX = re.compile("^[0-9]{4}-[\\w-]+\\.md*")


def adr_summary(
    env: MacrosPlugin,
    adr_path: str,
    adr_style: TYPE_ADRStyle,
    template_file: Optional[str] = None,
) -> str:
    absolute_path = Path(env.project_dir).joinpath(adr_path)
    parser = get_parser(adr_style)

    documents = [
        parser.parse(absolute_path.joinpath(f), env.conf["docs_dir"])
        for f in os.listdir(absolute_path)
        if os.path.isfile(absolute_path.joinpath(f)) and ADR_REGEX.match(f)
    ]

    return Jinja2Renderer.summary(
        documents=documents,
        mkdocs_base_path=Path(env.project_dir),
        template_file=template_file,
    )
