from unittest.mock import Mock

from mkdocs_macros_adr_summary import adr_summary


def test_adr_summary():
    assert (
        adr_summary(Mock())
        == "Here we will render an amazing summary for our ADR directory"
    )
