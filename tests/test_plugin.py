from pathlib import PosixPath
from unittest.mock import Mock, patch

from mkdocs_macros_adr_summary import adr_summary


def test_adr_summary():
    mkdocs_env = Mock()
    mkdocs_env.project_dir = "/some/path/to"
    mkdocs_env.conf = {"docs_dir": "/some/path/to"}

    fake_parser = Mock()
    fake_parser.parse.return_value = "someprocessedfile.md"

    with patch(
        "mkdocs_macros_adr_summary.plugin.get_parser", return_value=fake_parser
    ), patch(
        "mkdocs_macros_adr_summary.plugin.Jinja2Renderer.summary",
        return_value="TEST RETURN",
    ) as mock_summary, patch(
        "os.listdir",
        return_value=[
            "somefile.md",
            "0001-somevalidfile.md",
            "0001-someoth\erfile.md",
            "0001-someoth/erfile.md",
        ],
    ) as mock_listdir, patch(
        "os.path.isfile", return_value=True
    ):
        summary = adr_summary(env=mkdocs_env, adr_path="docs/adr")

    mock_listdir.assert_called_once_with(PosixPath("/some/path/to/docs/adr"))
    fake_parser.parse.assert_called_once_with(
        PosixPath("/some/path/to/docs/adr/0001-somevalidfile.md"),
        "/some/path/to",
    )
    mock_summary.assert_called_once_with(
        documents=["someprocessedfile.md"],
        mkdocs_base_path=PosixPath("/some/path/to"),
        template_file=None,
    )
    assert summary == "TEST RETURN"
