import pytest

from seez.ports.adapters.repositories import (
    SqlAlchemyCarRepository,
    SqlAlchemyMakeRepository,
    SqlAlchemyModelRepository,
    SqlAlchemySubModelRepository,
)


@pytest.fixture()
def car_repository():
    return SqlAlchemyCarRepository()


@pytest.fixture()
def model_repository():
    return SqlAlchemyModelRepository()


@pytest.fixture()
def submodel_repository():
    return SqlAlchemySubModelRepository()


@pytest.fixture()
def make_repository():
    return SqlAlchemyMakeRepository()
