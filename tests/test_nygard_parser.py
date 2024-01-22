from datetime import datetime
from pathlib import Path

import pytest

from mkdocs_macros_adr_summary.interfaces import ADRDocument
from mkdocs_macros_adr_summary.parser import NygardParser


@pytest.mark.parametrize(
    ["filename", "expected_statuses"],
    [
        ("valid.md", tuple(["Accepted"])),
        (
            "valid_multi_status.md",
            tuple(
                [
                    "Accepted",
                    "Supercedes [1. Record architecture decisions]"
                    "(0001-record-architecture-decisions.md)",
                ]
            ),
        ),
    ],
)
def test_parse_valid_document(filename: str, expected_statuses: tuple):
    assert NygardParser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}")
    ) == ADRDocument(
        filename=str(Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}")),
        title="1. Record architecture decisions",
        date=datetime.fromisoformat("2024-01-20").date(),
        statuses=expected_statuses,
    )


def test_parse_invalid_lines_delta():
    assert NygardParser.parse(
        Path(__file__).parent.joinpath("adr_docs/nygard/invalid_lines_delta.md")
    ) == ADRDocument(
        filename=str(
            Path(__file__).parent.joinpath("adr_docs/nygard/invalid_lines_delta.md")
        ),
        title="==INVALID_TITLE==",
        date=None,
        statuses=tuple(["==INVALID_STATUS=="]),
    )


@pytest.mark.parametrize(
    ["filename"],
    [("invalid_title_h3.md",), ("invalid_title_p.md",)],
)
def test_parse_invalid_title(filename: str):
    assert NygardParser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}")
    ) == ADRDocument(
        filename=str(Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}")),
        title="==INVALID_TITLE==",
        date=datetime.fromisoformat("2024-01-20").date(),
        statuses=tuple(["Accepted"]),
    )


@pytest.mark.parametrize(
    ["filename"],
    [("invalid_date_h3.md",), ("invalid_date_format.md",), ("invalid_date_blank.md",)],
)
def test_parse_invalid_date(filename: str):
    assert NygardParser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}")
    ) == ADRDocument(
        filename=str(Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}")),
        title="1. Record architecture decisions",
        date=None,
        statuses=tuple(["Accepted"]),
    )


@pytest.mark.parametrize(
    ["filename"],
    [("invalid_status_h3.md",)],
)
def test_parse_invalid_status(filename: str):
    assert NygardParser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}")
    ) == ADRDocument(
        filename=str(Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}")),
        title="1. Record architecture decisions",
        date=datetime.fromisoformat("2024-01-20").date(),
        statuses=tuple(["==INVALID_STATUS=="]),
    )
