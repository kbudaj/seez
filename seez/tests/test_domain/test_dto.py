import json
from datetime import datetime
from uuid import UUID

import pytest
from assertpy.assertpy import assert_that
from freezegun import freeze_time

from seez.aliases import CarPk
from seez.domain.dto import CarDTO, CarListDTO
from seez.domain.models import Car


@pytest.mark.postgres_db
class TestCarDTO:
    @freeze_time("2020-06-01 20:00:00")
    def test_from_model_to_json(
        self, make_factory, model_factory, submodel_factory, car_factory
    ):
        make_name = "Mercedes"
        model_name = "CSL"
        submodel_name = "CSL200"
        make = make_factory(name=make_name)
        model = model_factory(name=model_name, make=make)
        submodel = submodel_factory(name=submodel_name, model=model)
        car_pk = CarPk(UUID("b69e3c8c-0ea7-40f9-8141-9f5496523a85"))
        car = car_factory(
            pk=car_pk,
            active=True,
            year=2020,
            mileage=2000,
            price=100000,
            exterior_color="White",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            body_type=Car.BodyType.SUV,
            transmission=Car.Transmission.AUTOMATIC,
            fuel_type=Car.FuelType.PETROL,
            submodel=submodel,
        )
        dto = CarDTO.from_model(car)
        expected = {
            "pk": "b69e3c8c-0ea7-40f9-8141-9f5496523a85",
            "year": 2020,
            "mileage": 2000,
            "price": 100000,
            "exterior_color": "White",
            "created_at": "2020-06-01T20:00:00",
            "updated_at": "2020-06-01T20:00:00",
            "body_type": "SUV",
            "transmission": "AUTOMATIC",
            "fuel_type": "PETROL",
            "submodel": "CSL200",
            "model": "CSL",
            "make": "Mercedes",
        }
        assert_that(dto.json()).is_equal_to(json.dumps(expected))


@pytest.mark.postgres_db
class TestCarListDTO:
    @freeze_time("2020-06-01 20:00:00")
    def test_from_model_to_json(
        self, make_factory, model_factory, submodel_factory, car_factory
    ):
        make_name = "Mercedes"
        model_name = "CSL"
        submodel_name = "CSL200"
        make = make_factory(name=make_name)
        model = model_factory(name=model_name, make=make)
        submodel = submodel_factory(name=submodel_name, model=model)
        car_1_pk = CarPk(UUID("b69e3c8c-0ea7-40f9-8141-9f5496523a85"))
        car_2_pk = CarPk(UUID("bb04a84d-e3c2-4c63-8dd3-9b1401eae8ae"))
        car_1 = car_factory(
            pk=car_1_pk,
            active=True,
            year=2020,
            mileage=2000,
            price=100000,
            exterior_color="White",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            body_type=Car.BodyType.SUV,
            transmission=Car.Transmission.AUTOMATIC,
            fuel_type=Car.FuelType.PETROL,
            submodel=submodel,
        )
        car_2 = car_factory(
            pk=car_2_pk,
            active=True,
            year=2010,
            mileage=30000,
            price=30000,
            exterior_color="Black",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            body_type=Car.BodyType.SUV,
            transmission=Car.Transmission.AUTOMATIC,
            fuel_type=Car.FuelType.PETROL,
            submodel=submodel,
        )
        cars = [car_1, car_2]
        dto = CarListDTO.from_model(cars)

        expected = {
            "values": [
                {
                    "pk": "b69e3c8c-0ea7-40f9-8141-9f5496523a85",
                    "year": 2020,
                    "mileage": 2000,
                    "price": 100000,
                    "exterior_color": "White",
                    "created_at": "2020-06-01T20:00:00",
                    "updated_at": "2020-06-01T20:00:00",
                    "body_type": "SUV",
                    "transmission": "AUTOMATIC",
                    "fuel_type": "PETROL",
                    "submodel": "CSL200",
                    "model": "CSL",
                    "make": "Mercedes",
                },
                {
                    "pk": "bb04a84d-e3c2-4c63-8dd3-9b1401eae8ae",
                    "year": 2010,
                    "mileage": 30000,
                    "price": 30000,
                    "exterior_color": "Black",
                    "created_at": "2020-06-01T20:00:00",
                    "updated_at": "2020-06-01T20:00:00",
                    "body_type": "SUV",
                    "transmission": "AUTOMATIC",
                    "fuel_type": "PETROL",
                    "submodel": "CSL200",
                    "model": "CSL",
                    "make": "Mercedes",
                },
            ]
        }

        assert_that(dto.json()).is_equal_to(json.dumps(expected))
