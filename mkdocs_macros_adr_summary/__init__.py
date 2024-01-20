from mkdocs_macros.plugin import MacrosPlugin

from .plugin import adr_summary


def define_env(env: MacrosPlugin) -> None:
    env.macro(adr_summary)


__version__ = "0.0.0"
__version_tuple__ = (0, 0, 0)
