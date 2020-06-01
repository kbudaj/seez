import pytest

from seez.ports.adapters.repositories import SqlAlchemyCarRepository


@pytest.fixture()
def car_repository():
    return SqlAlchemyCarRepository()


@pytest.mark.postgres_db
class TestCarRepository:
    def test_get_by_pk(self, car_factory, car_repository):
        car1 = car_factory()
        result = car_repository.get_by_pk(car1.pk)
        assert result == car1

    def test_get_all(self, car_repository):
        assert len(car_repository.get_all()) == 0
