import os
import traceback
import typing
from importlib import util


class BaseTool:
    """Base class for all tools used with TRAVIS"""

    plugins = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.plugins[cls.__name__] = cls

    def tool_schema() -> typing.Dict:
        """Returns the schema used in the API request for this tool. Read the docs for more information."""
        pass

    def run_tool(**kwargs) -> typing.Dict[str, str]:
        """Runs the tool and returns a JSON object with the result or an error. This function must return a dict with either a 'result' or 'error' field"""
        pass


def load_module(path):
    name = os.path.split(path)[-1]
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

for fname in os.listdir(dirpath):
    # Load only "real modules"
    if (
        not fname.startswith(".")
        and not fname.startswith("__")
        and fname.endswith(".py")
    ):
        try:
            load_module(os.path.join(dirpath, fname))
        except Exception:
            traceback.print_exc()
