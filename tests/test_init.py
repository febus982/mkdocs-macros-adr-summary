from unittest.mock import Mock

from mkdocs_macros_adr_summary import adr_summary, define_env


def test_env_initialises_plugin():
    env = Mock()
    env.macro = Mock(return_value=None)

    define_env(env)

    env.macro.assert_called_once_with(adr_summary)
