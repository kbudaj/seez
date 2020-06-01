import factory

from seez.domain.models import Car
from seez.tests.factories import SQLAlchemyBase


class CarFactory(SQLAlchemyBase):
    pk = factory.LazyFunction(Car.next_pk)
    title = factory.Sequence(lambda n: f"Car title {n}")

    class Meta:
        model = Car
