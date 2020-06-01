import json
from datetime import datetime
from uuid import UUID

import pytest
from assertpy.assertpy import assert_that
from freezegun import freeze_time

from seez.aliases import CarPk, MakePk, ModelPk, SubModelPk
from seez.domain.dto import (
    CarDTO,
    CarListDTO,
    MakeDTO,
    MakeListDTO,
    ModelDTO,
    ModelListDTO,
    SubModelDTO,
    SubModelListDTO,
)
from seez.domain.models import Car


@pytest.mark.postgres_db
class TestCarDTO:
    @freeze_time("2020-06-01 20:00:00")
    def test_from_model_to_json(
        self, make_factory, model_factory, submodel_factory, car_factory
    ):
        make = make_factory(name="Mercedes")
        model = model_factory(name="CLS", make=make)
        submodel = submodel_factory(name="CLS200", model=model)
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
            "submodel": "CLS200",
            "model": "CLS",
            "make": "Mercedes",
        }
        assert_that(dto.json()).is_equal_to(json.dumps(expected))


@pytest.mark.postgres_db
class TestCarListDTO:
    @freeze_time("2020-06-01 20:00:00")
    def test_from_model_to_json(
        self, make_factory, model_factory, submodel_factory, car_factory
    ):
        make = make_factory(name="Mercedes")
        model = model_factory(name="CLS", make=make)
        submodel = submodel_factory(name="CLS200", model=model)
        car_1 = car_factory(
            pk=CarPk(UUID("b69e3c8c-0ea7-40f9-8141-9f5496523a85")),
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
            pk=CarPk(UUID("bb04a84d-e3c2-4c63-8dd3-9b1401eae8ae")),
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
                    "submodel": "CLS200",
                    "model": "CLS",
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
                    "submodel": "CLS200",
                    "model": "CLS",
                    "make": "Mercedes",
                },
            ]
        }

        assert_that(dto.json()).is_equal_to(json.dumps(expected))


@pytest.mark.postgres_db
class TestMakeDTO:
    @freeze_time("2020-06-01 20:00:00")
    def test_from_model_to_json(self, make_factory):
        make = make_factory(
            pk=MakePk(UUID("774c4c41-8a04-41d6-b5a0-854c01674958")),
            name="Mercedes",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        dto = MakeDTO.from_model(make)
        expected = {
            "pk": "774c4c41-8a04-41d6-b5a0-854c01674958",
            "name": "Mercedes",
            "created_at": "2020-06-01T20:00:00",
            "updated_at": "2020-06-01T20:00:00",
        }
        assert_that(dto.json()).is_equal_to(json.dumps(expected))


@pytest.mark.postgres_db
class TestMakeListDTO:
    @freeze_time("2020-06-01 20:00:00")
    def test_from_model_to_json(self, make_factory):
        make_1 = make_factory(
            pk=MakePk(UUID("774c4c41-8a04-41d6-b5a0-854c01674958")),
            name="Mercedes",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        make_2 = make_factory(
            pk=MakePk(UUID("94093c77-dd16-4120-861e-eae7f6ca24f7")),
            name="Audi",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        makes = [make_1, make_2]
        dto = MakeListDTO.from_model(makes)
        expected = {
            "values": [
                {
                    "pk": "774c4c41-8a04-41d6-b5a0-854c01674958",
                    "name": "Mercedes",
                    "created_at": "2020-06-01T20:00:00",
                    "updated_at": "2020-06-01T20:00:00",
                },
                {
                    "pk": "94093c77-dd16-4120-861e-eae7f6ca24f7",
                    "name": "Audi",
                    "created_at": "2020-06-01T20:00:00",
                    "updated_at": "2020-06-01T20:00:00",
                },
            ]
        }
        assert_that(dto.json()).is_equal_to(json.dumps(expected))


@pytest.mark.postgres_db
class TestModelDTO:
    @freeze_time("2020-06-01 20:00:00")
    def test_from_model_to_json(self, make_factory, model_factory):
        make = make_factory(
            pk=MakePk(UUID("774c4c41-8a04-41d6-b5a0-854c01674958")),
            name="Mercedes",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        model = model_factory(
            pk=ModelPk(UUID("2f88fa28-d8aa-4315-ad53-d05dacdcd920")),
            name="CLS",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            make=make,
        )
        dto = ModelDTO.from_model(model)
        expected = {
            "pk": "2f88fa28-d8aa-4315-ad53-d05dacdcd920",
            "name": "CLS",
            "make": "Mercedes",
            "created_at": "2020-06-01T20:00:00",
            "updated_at": "2020-06-01T20:00:00",
        }
        assert_that(dto.json()).is_equal_to(json.dumps(expected))


@pytest.mark.postgres_db
class TestModelListDTO:
    @freeze_time("2020-06-01 20:00:00")
    def test_from_model_to_json(self, make_factory, model_factory):
        make = make_factory(
            pk=MakePk(UUID("774c4c41-8a04-41d6-b5a0-854c01674958")),
            name="Mercedes",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        model_1 = model_factory(
            pk=ModelPk(UUID("2f88fa28-d8aa-4315-ad53-d05dacdcd920")),
            name="CLS",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            make=make,
        )
        model_2 = model_factory(
            pk=ModelPk(UUID("b8c5d732-eaf0-4c91-ab37-6af335b379d0")),
            name="CLA",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            make=make,
        )
        models = [model_1, model_2]
        dto = ModelListDTO.from_model(models)
        expected = {
            "values": [
                {
                    "pk": "2f88fa28-d8aa-4315-ad53-d05dacdcd920",
                    "name": "CLS",
                    "make": "Mercedes",
                    "created_at": "2020-06-01T20:00:00",
                    "updated_at": "2020-06-01T20:00:00",
                },
                {
                    "pk": "b8c5d732-eaf0-4c91-ab37-6af335b379d0",
                    "name": "CLA",
                    "make": "Mercedes",
                    "created_at": "2020-06-01T20:00:00",
                    "updated_at": "2020-06-01T20:00:00",
                },
            ]
        }
        assert_that(dto.json()).is_equal_to(json.dumps(expected))


@pytest.mark.postgres_db
class TestSubModelDTO:
    @freeze_time("2020-06-01 20:00:00")
    def test_from_model_to_json(self, make_factory, model_factory, submodel_factory):
        make = make_factory(
            pk=MakePk(UUID("774c4c41-8a04-41d6-b5a0-854c01674958")),
            name="Mercedes",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        model = model_factory(
            pk=ModelPk(UUID("2f88fa28-d8aa-4315-ad53-d05dacdcd920")),
            name="CLS",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            make=make,
        )
        submodel = submodel_factory(
            pk=SubModelPk(UUID("d563e365-4c36-4d7e-98c0-256befda20bf")),
            name="CLS200",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            model=model,
        )
        dto = SubModelDTO.from_model(submodel)
        expected = {
            "pk": "d563e365-4c36-4d7e-98c0-256befda20bf",
            "name": "CLS200",
            "make": "Mercedes",
            "model": "CLS",
            "created_at": "2020-06-01T20:00:00",
            "updated_at": "2020-06-01T20:00:00",
        }
        assert_that(dto.json()).is_equal_to(json.dumps(expected))


@pytest.mark.postgres_db
class TestSubModelListDTO:
    @freeze_time("2020-06-01 20:00:00")
    def test_from_model_to_json(self, make_factory, model_factory, submodel_factory):
        make = make_factory(
            pk=MakePk(UUID("774c4c41-8a04-41d6-b5a0-854c01674958")),
            name="Mercedes",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        model_1 = model_factory(
            pk=ModelPk(UUID("2f88fa28-d8aa-4315-ad53-d05dacdcd920")),
            name="CLS",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            make=make,
        )
        model_2 = model_factory(
            pk=ModelPk(UUID("68ba3e53-dffe-40b4-9ba9-519a8e252dd1")),
            name="CLA",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            make=make,
        )
        submodel_1 = submodel_factory(
            pk=SubModelPk(UUID("d563e365-4c36-4d7e-98c0-256befda20bf")),
            name="CLS200",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            model=model_1,
        )
        submodel_2 = submodel_factory(
            pk=SubModelPk(UUID("c7074111-b1e9-418e-be93-20d5c77011c8")),
            name="CLA500",
            active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            model=model_2,
        )
        submodels = [submodel_1, submodel_2]
        dto = SubModelListDTO.from_model(submodels)
        expected = {
            "values": [
                {
                    "pk": "d563e365-4c36-4d7e-98c0-256befda20bf",
                    "name": "CLS200",
                    "make": "Mercedes",
                    "model": "CLS",
                    "created_at": "2020-06-01T20:00:00",
                    "updated_at": "2020-06-01T20:00:00",
                },
                {
                    "pk": "c7074111-b1e9-418e-be93-20d5c77011c8",
                    "name": "CLA500",
                    "make": "Mercedes",
                    "model": "CLA",
                    "created_at": "2020-06-01T20:00:00",
                    "updated_at": "2020-06-01T20:00:00",
                },
            ]
        }
        assert_that(dto.json()).is_equal_to(json.dumps(expected))
