from datetime import datetime
from random import randint

import factory

from seez.domain.models import Car, Make, Model, SubModel
from seez.tests.factories import SQLAlchemyBase


class MakeFactory(SQLAlchemyBase):
    pk = factory.LazyFunction(Make.next_pk)
    name = factory.Sequence(lambda n: f"Make {n}")
    active = True
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = Make


class ModelFactory(SQLAlchemyBase):
    pk = factory.LazyFunction(Model.next_pk)
    name = factory.Sequence(lambda n: f"Car model {n}")
    active = True
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    make = factory.SubFactory(MakeFactory)

    make_pk = factory.SelfAttribute("make.pk")

    class Meta:
        model = Model
        exclude = ("make",)


class SubmodelFactory(SQLAlchemyBase):
    pk = factory.LazyFunction(SubModel.next_pk)
    name = factory.Sequence(lambda n: f"Sub model {n}")
    active = True
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    model = factory.SubFactory(ModelFactory)

    model_pk = factory.SelfAttribute("model.pk")

    class Meta:
        model = SubModel
        exclude = ("model",)


class CarFactory(SQLAlchemyBase):
    pk = factory.LazyFunction(Car.next_pk)
    active = True
    year = factory.LazyFunction(lambda: randint(1920, 2020))
    mileage = factory.LazyFunction(lambda: randint(0, 500000))
    price = factory.LazyFunction(lambda: randint(1000, 9000000))
    exterior_color = factory.Sequence(lambda n: f"Color {n}")
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)
    body_type = Car.BodyType.SEDAN
    transmission = Car.Transmission.AUTOMATIC
    fuel_type = Car.FuelType.PETROL

    submodel = factory.SubFactory(SubmodelFactory)

    submodel_pk = factory.SelfAttribute("submodel.pk")

    class Meta:
        model = Car
        exclude = ("submodel",)
