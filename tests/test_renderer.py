from datetime import datetime
from pathlib import Path, PosixPath
from unittest.mock import Mock, patch

import pytest
from jinja2 import Environment, FileSystemLoader

from mkdocs_macros_adr_summary.interfaces import ADRDocument
from mkdocs_macros_adr_summary.renderer import Jinja2Renderer


@pytest.mark.parametrize(
    ["template_file", "expected_path", "expected_template"],
    [
        pytest.param(
            None,
            Path(__file__).parent.parent.joinpath("mkdocs_macros_adr_summary"),
            "template.jinja",
            id="no_template_file",
        ),
        pytest.param(
            "path/to/template/custom.jinja",
            Path("/path/to/mkdocs"),
            "path/to/template/custom.jinja",
            id="custom_template_file",
        ),
    ],
)
def test_jinja_renderer_uses_default_template_if_no_template_file(
    template_file: str, expected_path: PosixPath, expected_template: str
):
    loader = Mock(spec=FileSystemLoader)
    env = Mock(spec=Environment)
    template = Mock()
    template.render.return_value = "SOME RETURN VALUE"
    env.get_template.return_value = template

    with (
        patch(
            "mkdocs_macros_adr_summary.renderer.FileSystemLoader",
            return_value=loader,
        ) as mock_loader,
        patch(
            "mkdocs_macros_adr_summary.renderer.Environment", return_value=env
        ) as mock_env,
    ):
        Jinja2Renderer.summary(
            documents=[
                ADRDocument(
                    file_path="something",
                    title="something",
                    date=datetime.now(),
                    statuses=["accepted"],
                )
            ],
            mkdocs_base_path=Path("/path/to/mkdocs"),
            template_file=template_file,
        )

    # Assert
    mock_loader.assert_called_once_with(searchpath=expected_path)
    mock_env.assert_called_once_with(
        loader=loader,
        autoescape=True,
    )
    env.get_template.assert_called_once_with(expected_template)
