from typing import Iterable

from .interfaces import ADRDocument


class Jinja2Renderer:
    @staticmethod
    def summary(documents: Iterable[ADRDocument]) -> str:
        output = "<ul>"
        output += "".join([f"<li>{d.filename}</li>" for d in documents])
        output += "</ul>"
        return output
