import factory

from seez.tests.factories import SQLAlchemyBase

from seez.domain.models import Car


class CarFactory(SQLAlchemyBase):
    pk = factory.LazyFunction(Car.next_pk)
    title = factory.Sequence(lambda n: f"Car title {n}")

    class Meta:
        model = Car
