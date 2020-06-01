import importlib
import os
from typing import Any, List

import pytest
from pytest_factoryboy import register

from seez.infrastructure.scopes import TestTransactionalScope
from seez.main import configure_haps
from seez.tests.fixtures.database import *  # noqa
from seez.tests.fixtures.repositories import *  # noqa


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        "--run-migrations", action="store_true", dest="run_migrations", default=False
    )


FACTORY_MODULES = ("seez.tests.factories.seez",)

for factory_module in FACTORY_MODULES:
    factories = importlib.import_module(factory_module)
    for k, v in factories.__dict__.items():
        if k.startswith("_"):
            continue

        if k.endswith("Factory") and not v._meta.abstract:
            register(v, _name=getattr(v, "_model_name", None))


@pytest.fixture(autouse=True, scope="session")
def configure_container():
    profiles: List[str] = os.environ.get("HAPS_PROFILES", "").split(",")
    if "tests" not in profiles:
        profiles.append("tests")
        os.environ["HAPS_PROFILES"] = ",".join(profiles)
    configure_haps(transactional_scope=TestTransactionalScope)
