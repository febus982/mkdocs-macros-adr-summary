from mkdocs_macros_adr_summary.interfaces import ADRDocument
from mkdocs_macros_adr_summary.parser import ADRNygardParser


def test_parser():
    assert ADRNygardParser.parse("something") == ADRDocument(filename="something")
