from datetime import datetime
from typing import List, Optional

from seez.aliases import (
    CarPk,
    Color,
    MakeName,
    Mileage,
    ModelName,
    Price,
    SubModelName,
    Year,
)
from seez.domain.models import Car
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
    __root__: List[CarDTO]

    @classmethod
    def from_model(cls, cars: List[Car]) -> "CarListDTO":
        car_dtos = []
        for car in cars:
            car_dtos.append(CarDTO.from_model(car))
        return cls(__root__=car_dtos)
