from mkdocs_macros_adr_summary.interfaces import ADRDocument
from mkdocs_macros_adr_summary.renderer import Jinja2Renderer


def test_jinja_renderer():
    summary = Jinja2Renderer.summary(documents=[ADRDocument(filename="something")])
    assert summary == "<ul><li>something</li></ul>"
