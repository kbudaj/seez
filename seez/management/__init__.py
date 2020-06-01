import pkgutil
import sys
from collections import defaultdict
from functools import lru_cache
from importlib import import_module
from typing import Dict, List

from seez.management.commands import ManagementCommand
from seez.management.exceptions import BaseCommandException


class ManagementUtility:
    commands_dir_path: str

    def __init__(
        self, module_name: str, commands_dir_path: str, argv: List[str] = None
    ) -> None:
        self.argv = argv or sys.argv[:]
        self.commands_dir_path = commands_dir_path
        self.module_name = module_name

    def execute(self) -> None:
        try:
            sub_command = self.argv[1]
        except IndexError:
            sub_command = "help"

        if sub_command == "help":
            sys.stdout.write(self.list_commands() + "\n")
        else:
            try:
                self.fetch_command(sub_command).run_from_argv(self.argv[2:])
            except BaseCommandException as e:
                self.handle_custom_exception(e)

    def list_commands(self) -> str:
        commands_dict: Dict[str, List[str]] = defaultdict(list)
        usage = ["", "Available sub-commands:"]

        for name, app in get_commands(self.module_name, self.commands_dir_path).items():
            commands_dict[app].append(name)

        for app in sorted(commands_dict):
            usage.append("")
            usage.append(f"[{app}]")
            for name in sorted(commands_dict[app]):
                usage.append(f"    {name}")

        return "\n".join(usage)

    def fetch_command(self, sub_command_name: str) -> ManagementCommand:
        """Loads command with given name."""

        available_commands = get_commands(self.module_name, self.commands_dir_path)

        try:
            module_name = available_commands[sub_command_name]
        except KeyError:
            sys.stderr.write(f"Unknown command: {sub_command_name}")
            sys.exit(1)

        return load_command_class(module_name, sub_command_name)

    @classmethod
    def handle_custom_exception(cls, exception: BaseCommandException) -> None:
        msg = exception.msg_template.format(*exception.args)
        sys.stderr.write(msg)
        sys.exit(1)


@lru_cache(maxsize=None)
def get_commands(module_name: str, commands_dir_path: str) -> Dict[str, str]:
    return {name: module_name for name in find_commands(commands_dir_path)}


def find_commands(command_dir: str) -> List[str]:
    return [
        name
        for _, name, is_pkg in pkgutil.iter_modules([command_dir])
        if not is_pkg and not name.startswith("_")
    ]


def load_command_class(package_name: str, command_name: str) -> ManagementCommand:
    module = import_module(f"{package_name}.management.commands.{command_name}")

    return module.Command()  # type: ignore


def execute_from_command_line(
    module_name: str, commands_dir_path: str, argv: List[str] = None
) -> None:
    ManagementUtility(module_name, commands_dir_path, argv).execute()
