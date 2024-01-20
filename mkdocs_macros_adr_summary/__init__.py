from functools import partial

from mkdocs_macros.plugin import MacrosPlugin

from .plugin import adr_summary


def define_env(env: MacrosPlugin) -> None:
    # We could use the decorator here, but it would be more complex to test
    env.macro(partial(adr_summary, env), "adr_summary")


__version__ = "0.0.0"
__version_tuple__ = (0, 0, 0)
