from functools import partial
from unittest.mock import Mock

from mkdocs_macros_adr_summary import adr_summary, define_env


def test_env_initialises_plugin():
    mocked_env = Mock()
    mocked_env.macro = Mock(return_value=None)

    define_env(mocked_env)

    mocked_env.macro.assert_called_once()
    # There is probably a nicer way to check a `functools.partial()` argument
    macro_call_args = mocked_env.macro.call_args_list[0].args
    # Check we called `env.macro` with 2 args
    assert len(macro_call_args) == 2
    # First argument should be `partial(adr_summary, mocked_env)`
    assert isinstance(macro_call_args[0], partial)
    partial_func: partial = macro_call_args[0]
    assert partial_func.func == adr_summary
    assert partial_func.args == (mocked_env,)
    # Second argument
    assert macro_call_args[1] == "adr_summary"
