from datetime import datetime
from typing import List, Optional

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
from seez.domain.models import Car, Make, Model, SubModel
from seez.infrastructure.dto import DTO


class CarDTO(DTO):
    pk: CarPk
    year: Year
    mileage: Optional[Mileage]
    price: Optional[Price]
    exterior_color: Optional[Color]
    created_at: datetime
    updated_at: datetime
    body_type: Optional[Car.BodyType]
    transmission: Optional[Car.Transmission]
    fuel_type: Optional[Car.FuelType]
    submodel: SubModelName
    model: ModelName
    make: MakeName

    @classmethod
    def from_model(cls, car: Car) -> "CarDTO":
        return cls(
            pk=car.pk,
            year=car.year,
            mileage=car.mileage,
            price=car.price,
            exterior_color=car.exterior_color,
            created_at=car.created_at,
            updated_at=car.updated_at,
            body_type=car.body_type,
            transmission=car.transmission,
            fuel_type=car.fuel_type,
            submodel=car.submodel_name,
            model=car.model_name,
            make=car.make_name,
        )


class CarListDTO(DTO):
    values: List[CarDTO]

    @classmethod
    def from_model(cls, cars: List[Car]) -> "CarListDTO":
        car_dtos = []
        for car in cars:
            car_dtos.append(CarDTO.from_model(car))
        return cls(values=car_dtos)


class MakeDTO(DTO):
    pk: MakePk
    name: MakeName
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, make: Make) -> "MakeDTO":
        return cls(
            pk=make.pk,
            name=make.name,
            created_at=make.created_at,
            updated_at=make.updated_at,
        )


class MakeListDTO(DTO):
    values: List[MakeDTO]

    @classmethod
    def from_model(cls, makes: List[MakeDTO]) -> "MakeListDTO":
        make_dtos = []
        for make in makes:
            make_dtos.append(MakeDTO.from_model(make))
        return cls(values=make_dtos)


class ModelDTO(DTO):
    pk: ModelPk
    name: ModelName
    make: MakeName
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, model: Model) -> "ModelDTO":
        return cls(
            pk=model.pk,
            name=model.name,
            make=model.make.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class ModelListDTO(DTO):
    values: List[ModelDTO]

    @classmethod
    def from_model(cls, models: List[Model]) -> "ModelListDTO":
        model_dtos = []
        for model in models:
            model_dtos.append(ModelDTO.from_model(model))
        return cls(values=model_dtos)


class SubModelDTO(DTO):
    pk: SubModelPk
    name: SubModelName
    make: MakeName
    model: ModelName
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, submodel: SubModel) -> "SubModelDTO":
        return cls(
            pk=submodel.pk,
            name=submodel.name,
            make=submodel.model.make.name,
            model=submodel.model.name,
            created_at=submodel.created_at,
            updated_at=submodel.updated_at,
        )


class SubModelListDTO(DTO):
    values: List[SubModelDTO]

    @classmethod
    def from_model(cls, submodels: List[SubModel]) -> "SubModelListDTO":
        submodel_dtos = []
        for submodel in submodels:
            submodel_dtos.append(SubModelDTO.from_model(submodel))
        return cls(values=submodel_dtos)
