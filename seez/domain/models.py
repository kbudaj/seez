import datetime
from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4

from seez.aliases import (
    CarPk,
    Color,
    MakeName,
    MakePk,
    Mileage,
    ModelName,
    ModelPk,
    Price,
    SubModelName,
    SubModelPk,
    Year,
)
from seez.infrastructure.models import AggregateRoot


@dataclass(unsafe_hash=False, eq=False)
class Car(AggregateRoot):
    pk: CarPk
    active: bool
    year: Year
    mileage: Mileage
    price: Price
    exterior_color: Color
    created_at: datetime
    updated_at: datetime

    make_pk: MakePk
    model_id: ModelPk
    submodel_id: SubModelPk

    _body_type: "Car.BodyType"
    _transmission: "Car.Transmission"
    _fuel_type: "Car.FuelType"

    class BodyType(Enum):
        COUPE = "COUPE"
        SEDAN = "SEDAN"
        SUV = "SUV"
        HATCHBACK = "HATCHBACK"
        CONVERTIBLE = "CONVERTIBLE"

    class Transmission(Enum):
        AUTOMATIC = "AUTOMATIC"
        MANUAL = "MANUAL"

    class FualType(Enum):
        PETROL = "PETROL"
        HYBRID = "HYBRID"

    @classmethod
    def next_pk(cls) -> CarPk:
        return CarPk(uuid4())

    @classmethod
    def create_new(cls, title: str) -> "Car":
        return cls(pk=cls.next_pk(), title=title)

    @property
    def body_type(self) -> "Car.BodyType":
        return self._body_type

    @property
    def transmission(self) -> "Car.Transmission":
        return self._transmission

    @property
    def fuel_type(self) -> "Car.FuelType":
        return self._fuel_type


@dataclass(unsafe_hash=False, eq=False)
class Make(AggregateRoot):
    pk: MakePk
    name: MakeName
    active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def next_pk(cls) -> MakePk:
        return MakePk(uuid4())


@dataclass(unsafe_hash=False, eq=False)
class Model(AggregateRoot):
    pk: ModelPk
    name: ModelName
    active: bool
    make_id: UUID
    created_at: datetime
    updated_at: datetime

    @classmethod
    def next_pk(cls) -> ModelPk:
        return ModelPk(uuid4())


@dataclass(unsafe_hash=False, eq=False)
class SubModel(AggregateRoot):
    pk: SubModelPk
    name: SubModelName
    active: bool
    model_id: UUID
    created_at: datetime
    updated_at: datetime

    @classmethod
    def next_pk(cls) -> SubModelPk:
        return SubModelPk(uuid4())
