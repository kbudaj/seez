import configparser

import mypy.api


class MypyError(Exception):
    pass


def mypy_test(cfg_path: str) -> None:
    cfg = configparser.ConfigParser()
    cfg.read(cfg_path)
    test_paths = cfg.get("tool:pytest", "testpaths").split()
    stdout, stderr, exit_status = mypy.api.run(test_paths)

    if exit_status:
        raise MypyError(stderr + stdout)
