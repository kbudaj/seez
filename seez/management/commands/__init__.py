import argparse
import sys
from abc import ABC, abstractmethod
from typing import Any, List, Optional, TextIO


class ManagementCommand(ABC):
    description: str = "Command description"
    args: Optional[argparse.Namespace] = None

    def __init__(self) -> None:
        self.stdout = OutputWrapper(sys.stdout)
        self.stderr = OutputWrapper(sys.stderr)

    def init(self, args: List[Any]) -> None:
        parser = argparse.ArgumentParser(description=self.description)
        self.define_args(parser)
        self.args = parser.parse_args(args=args)

    def run_from_argv(self, args: List[Any] = []) -> None:
        self.init(args)
        self.handle()

    def define_args(self, parser: argparse.ArgumentParser) -> None:
        pass

    @abstractmethod
    def handle(self) -> None:
        pass


class OutputWrapper:
    def __init__(self, output: TextIO, ending: str = "\n") -> None:
        super().__init__()
        self._output = output
        self.ending = ending

    def __getattr__(self, name: str) -> Any:
        return getattr(self._output, name)

    def write(self, message: str, ending: str = None) -> None:
        ending = self.ending if ending is None else ending

        if ending and not message.endswith(ending):
            message += ending

        self._output.write(message)
