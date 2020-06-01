import configparser
import subprocess
from typing import Any


class FlakeError(Exception):
    def __init__(self, message: str, *args: Any, **kwargs: Any) -> None:
        message = "Flake8 check Failed to successfully complete.\n" + message
        super().__init__(message, *args, **kwargs)  # type: ignore


def flake_test(cfg_path: str) -> None:
    cfg = configparser.ConfigParser()
    cfg.read(cfg_path)
    test_paths = cfg.get("tool:pytest", "testpaths")
    max_line_length = cfg.get("tool:pytest", "flake8-max-line-length")
    ignores = cfg.get("tool:pytest", "flake8-ignore")
    excludes = cfg.get("tool:pytest", "flake8-exclude")

    command = f"flake8 {test_paths}"
    if max_line_length:
        command = f"{command} --max-line-length={max_line_length} --ignore={ignores} --exclude={excludes}"

    result = subprocess.run(
        command,
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    if result.returncode:
        raise FlakeError(result.stdout + result.stderr)
