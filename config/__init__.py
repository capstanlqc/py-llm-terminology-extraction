# __init__.py

import pathlib
import tomllib

path = pathlib.Path(__file__).parent
with path.open(mode="rb") as fp:
    settings = tomli.load(fp)
