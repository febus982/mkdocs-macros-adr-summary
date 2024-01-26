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

from pathlib import Path
from typing import Iterable, Optional

from jinja2 import Environment, FileSystemLoader

from .interfaces import ADRDocument


class Jinja2Renderer:
    @staticmethod
    def summary(
        documents: Iterable[ADRDocument],
        mkdocs_base_path: Path,
        template_file: Optional[str] = None,
    ) -> str:
        if template_file:
            template_env = Environment(
                loader=FileSystemLoader(searchpath=mkdocs_base_path),
                autoescape=True,
            )
            template = template_env.get_template(template_file)
        else:
            template_env = Environment(
                loader=FileSystemLoader(searchpath=Path(__file__).parent),
                autoescape=True,
            )
            template = template_env.get_template("template.jinja")

        return template.render(documents=documents)
