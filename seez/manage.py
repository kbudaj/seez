import sys
from pathlib import Path

from seez.main import configure_haps
from seez.management import execute_from_command_line

configure_haps()
execute_from_command_line(
    "seez",
    str(Path(__file__).resolve().parent.joinpath("management/commands")),
    sys.argv,
)
