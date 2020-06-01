from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

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
    mileage: Optional[Mileage]
    price: Optional[Price]
    exterior_color: Optional[Color]
    created_at: datetime
    updated_at: datetime

    submodel_pk: SubModelPk

    _body_type: Optional["Car.BodyType"]
    _transmission: Optional["Car.Transmission"]
    _fuel_type: Optional["Car.FuelType"]
    _submodel: "SubModel"

    class BodyType(Enum):
        COUPE = "COUPE"
        SEDAN = "SEDAN"
        SUV = "SUV"
        HATCHBACK = "HATCHBACK"
        CONVERTIBLE = "CONVERTIBLE"
        VAN = "VAN"
        SPORTS = "SPORTS"
        TRUCK = "TRUCK"
        WAGON = "WAGON"
        LUXURY = "LUXURY"

        def __str__(self) -> str:
            return self.name

    class Transmission(Enum):
        AUTOMATIC = "AUTOMATIC"
        MANUAL = "MANUAL"

        def __str__(self) -> str:
            return self.name

    class FuelType(Enum):
        PETROL = "PETROL"
        HYBRID = "HYBRID"
        DIESEL = "DIESEL"
        ELECTRICITY = "ELECTRICITY"

        def __str__(self) -> str:
            return self.name

    def __init__(
        self,
        pk: CarPk,
        active: bool,
        year: Year,
        mileage: Mileage,
        price: Optional[Price],
        exterior_color: Optional[Color],
        created_at: datetime,
        updated_at: datetime,
        submodel_pk: SubModelPk,
        body_type: Optional[BodyType],
        transmission: Optional[Transmission],
        fuel_type: Optional[FuelType],
    ):
        self.pk = pk
        self.active = active
        self.year = year
        self.mileage = mileage
        self.price = price
        self.exterior_color = exterior_color
        self.created_at = created_at
        self.updated_at = updated_at
        self.submodel_pk = submodel_pk
        self._body_type = body_type
        self._transmission = transmission
        self._fuel_type = fuel_type

    @classmethod
    def next_pk(cls) -> CarPk:
        return CarPk(uuid4())

    @classmethod
    def create_new(
        cls,
        year: Year,
        mileage: Mileage,
        submodel_pk: SubModelPk,
        price: Optional[Price],
        exterior_color: Color,
        body_type: Optional[BodyType],
        transmission: Optional[Transmission],
        fuel_type: Optional[FuelType],
    ) -> "Car":
        return cls(
            pk=cls.next_pk(),
            active=True,
            year=year,
            mileage=mileage,
            price=price,
            exterior_color=exterior_color,
            submodel_pk=submodel_pk,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            body_type=body_type,
            transmission=transmission,
            fuel_type=fuel_type,
        )

    @property
    def body_type(self) -> Optional["Car.BodyType"]:
        return self._body_type

    @property
    def transmission(self) -> Optional["Car.Transmission"]:
        return self._transmission

    @property
    def fuel_type(self) -> Optional["Car.FuelType"]:
        return self._fuel_type

    @property
    def submodel_name(self) -> "SubModelName":
        return self._submodel.name

    @property
    def model_name(self) -> "ModelName":
        return self._submodel.model.name

    @property
    def make_name(self) -> "MakeName":
        return self._submodel.model.make.name


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

    @classmethod
    def create_new(cls, name: MakeName) -> "Make":
        return cls(
            pk=cls.next_pk(),
            name=name,
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )


@dataclass(unsafe_hash=False, eq=False)
class Model(AggregateRoot):
    pk: ModelPk
    name: ModelName
    active: bool
    make_pk: MakePk
    created_at: datetime
    updated_at: datetime

    _make: Make

    def __init__(
        self,
        pk: ModelPk,
        name: ModelName,
        active: bool,
        make_pk: MakePk,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        self.pk = pk
        self.name = name
        self.active = active
        self.make_pk = make_pk
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def next_pk(cls) -> ModelPk:
        return ModelPk(uuid4())

    @property
    def make(self) -> Make:
        return self._make


@dataclass(unsafe_hash=False, eq=False)
class SubModel(AggregateRoot):
    pk: SubModelPk
    name: SubModelName
    active: bool
    model_pk: ModelPk
    created_at: datetime
    updated_at: datetime

    _model: Model

    def __init__(
        self,
        pk: SubModelPk,
        name: SubModelName,
        active: bool,
        model_pk: ModelPk,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        self.pk = pk
        self.name = name
        self.active = active
        self.model_pk = model_pk
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def next_pk(cls) -> SubModelPk:
        return SubModelPk(uuid4())

    @property
    def model(self) -> Model:
        return self._model
