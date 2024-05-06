from datetime import datetime
from pathlib import Path
from typing import Optional

import pytest

from mkdocs_macros_adr_summary.parser import NygardParser


@pytest.mark.parametrize(
    ["filename", "expected_id", "expected_statuses"],
    [
        (
            "0001-valid.md",
            1,
            ("Accepted",),
        ),
        (
            "valid_multi_status.md",
            None,
            (
                "Accepted",
                "Supercedes [1. Record architecture decisions]"
                "(0001-record-architecture-decisions.md)",
            ),
        ),
    ],
)
def test_parse_valid_document(
    filename: str,
    expected_statuses: tuple,
    expected_id: Optional[int],
    adr_document_factory,
) -> None:
    doc = NygardParser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}"),
        base_path=Path(__file__).parent,
    )
    doc2 = adr_document_factory(
        file_path=f"../adr_docs/nygard/{filename}",
        title="1. Record architecture decisions",
        date=datetime.fromisoformat("2024-01-20").date(),
        status=expected_statuses[-1],
        statuses=expected_statuses,
        document_id=expected_id,
    )
    assert doc == doc2


def test_can_parse_invalid_lines_delta(adr_document_factory):
    assert NygardParser.parse(
        Path(__file__).parent.joinpath("adr_docs/nygard/invalid_lines_delta.md"),
        base_path=Path(__file__).parent,
    ) == adr_document_factory(
        file_path="../adr_docs/nygard/invalid_lines_delta.md",
        title="1. Record architecture decisions",
        date=datetime.fromisoformat("2024-01-20").date(),
        status="Accepted",
        statuses=("Accepted",),
    )


@pytest.mark.parametrize(
    ["filename"],
    [("invalid_title_h3.md",), ("invalid_title_p.md",)],
)
def test_parse_invalid_title(filename: str, adr_document_factory):
    document = NygardParser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}"),
        base_path=Path(__file__).parent,
    )
    assert (
        document.title
        == adr_document_factory(
            title=None,
        ).title
    )


@pytest.mark.parametrize(
    ["filename"],
    [
        ("invalid_date_h3.md",),
        ("invalid_date_format.md",),
        ("invalid_date_blank.md",),
        ("invalid_date_broken_file.md",),
    ],
)
def test_parse_invalid_date(filename: str):
    document = NygardParser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}"),
        base_path=Path(__file__).parent,
    )
    assert document.date is None


@pytest.mark.parametrize(
    ["filename"],
    [
        ("invalid_status_h3.md",),
        ("invalid_status_broken_file.md",),
    ],
)
def test_parse_invalid_status(filename: str, adr_document_factory):
    document = NygardParser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/nygard/{filename}"),
        base_path=Path(__file__).parent,
    )

    assert (
        document.statuses
        == adr_document_factory(
            status=None,
            statuses=tuple(),
        ).statuses
    )
