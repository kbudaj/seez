from datetime import datetime
from uuid import UUID

import pytest
from assertpy.assertpy import assert_that
from fastapi.testclient import TestClient
from freezegun import freeze_time

from seez.aliases import CarPk, MakePk, ModelPk, SubModelPk
from seez.api.app import app
from seez.domain.models import Car


@pytest.fixture
def api_client():
    return TestClient(app)


@pytest.mark.postgres_db
@freeze_time("2020-06-02 10:00")
def test_get_makes(api_client, make_factory):
    make_factory(
        pk=MakePk(UUID("774c4c41-8a04-41d6-b5a0-854c01674958")),
        name="Mercedes",
        active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    make_factory(
        pk=MakePk(UUID("94093c77-dd16-4120-861e-eae7f6ca24f7")),
        name="Audi",
        active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    response = api_client.get("/make/")
    assert_that(response.status_code).is_equal_to(200)
    expected = {
        "values": [
            {
                "pk": "774c4c41-8a04-41d6-b5a0-854c01674958",
                "name": "Mercedes",
                "created_at": "2020-06-02T10:00:00",
                "updated_at": "2020-06-02T10:00:00",
            },
            {
                "pk": "94093c77-dd16-4120-861e-eae7f6ca24f7",
                "name": "Audi",
                "created_at": "2020-06-02T10:00:00",
                "updated_at": "2020-06-02T10:00:00",
            },
        ]
    }
    assert_that(response.json()).is_equal_to(expected)


@pytest.mark.postgres_db
@freeze_time("2020-06-02 10:00")
def test_get_models(make_factory, model_factory, api_client):
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
    response = api_client.get("/model/")
    assert_that(response.status_code).is_equal_to(200)
    expected = {
        "values": [
            {
                "pk": "2f88fa28-d8aa-4315-ad53-d05dacdcd920",
                "name": "CLS",
                "make": "Mercedes",
                "created_at": "2020-06-02T10:00:00",
                "updated_at": "2020-06-02T10:00:00",
            },
            {
                "pk": "b8c5d732-eaf0-4c91-ab37-6af335b379d0",
                "name": "CLA",
                "make": "Mercedes",
                "created_at": "2020-06-02T10:00:00",
                "updated_at": "2020-06-02T10:00:00",
            },
        ]
    }
    assert_that(response.json()).is_equal_to(expected)


@pytest.mark.postgres_db
@freeze_time("2020-06-02 10:00")
def test_get_submodels(api_client, model_factory, make_factory, submodel_factory):
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
    response = api_client.get("/submodel/")
    assert_that(response.status_code).is_equal_to(200)
    expected = {
        "values": [
            {
                "pk": "d563e365-4c36-4d7e-98c0-256befda20bf",
                "name": "CLS200",
                "make": "Mercedes",
                "model": "CLS",
                "created_at": "2020-06-02T10:00:00",
                "updated_at": "2020-06-02T10:00:00",
            },
            {
                "pk": "c7074111-b1e9-418e-be93-20d5c77011c8",
                "name": "CLA500",
                "make": "Mercedes",
                "model": "CLA",
                "created_at": "2020-06-02T10:00:00",
                "updated_at": "2020-06-02T10:00:00",
            },
        ]
    }
    assert_that(response.json()).is_equal_to(expected)


@pytest.mark.postgres_db
@freeze_time("2020-06-02 10:00")
def test_get_cars(api_client, make_factory, model_factory, submodel_factory, car_factory):
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
    response = api_client.get("/car/")
    assert_that(response.status_code).is_equal_to(200)
    expected = {
        "values": [
            {
                "pk": "b69e3c8c-0ea7-40f9-8141-9f5496523a85",
                "year": 2020,
                "mileage": 2000,
                "price": 100000,
                "exterior_color": "White",
                "created_at": "2020-06-02T10:00:00",
                "updated_at": "2020-06-02T10:00:00",
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
                "created_at": "2020-06-02T10:00:00",
                "updated_at": "2020-06-02T10:00:00",
                "body_type": "SUV",
                "transmission": "AUTOMATIC",
                "fuel_type": "PETROL",
                "submodel": "CLS200",
                "model": "CLS",
                "make": "Mercedes",
            },
        ]
    }
    assert_that(response.json()).is_equal_to(expected)


@pytest.mark.postgres_db
@freeze_time("2020-06-02 10:00")
@pytest.mark.parametrize(
    "mileage, price, q_mileage_min, q_mileage_max, q_price_min, q_price_max, result",
    [
        (1000, 1000, None, None, None, None, 1),
        (1000, 1000, 1000, None, None, None, 1),
        (1000, 1000, 1001, None, None, None, 0),
        (1000, 1000, 1000, 1000, None, None, 1),
        (1000, 1000, None, None, 1000, None, 1),
        (1000, 1000, None, None, 1000, 1000, 1),
        (1000, 1000, None, None, 900, 999, 0),
        (1000, 1000, None, None, None, 999, 0),
        (1000, 1000, None, None, None, 1001, 1),
        (1000, 1000, 1000, 1000, 1000, 1000, 1),
    ],
)
def test_get_cars(
    api_client,
    make_factory,
    model_factory,
    submodel_factory,
    car_factory,
    mileage,
    price,
    q_price_min,
    q_price_max,
    q_mileage_min,
    q_mileage_max,
    result,
):
    make = make_factory(name="Mercedes")
    model = model_factory(name="CLS", make=make)
    submodel = submodel_factory(name="CLS200", model=model)
    car = car_factory(
        pk=CarPk(UUID("b69e3c8c-0ea7-40f9-8141-9f5496523a85")),
        active=True,
        year=2020,
        mileage=mileage,
        price=price,
        exterior_color="White",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        body_type=Car.BodyType.SUV,
        transmission=Car.Transmission.AUTOMATIC,
        fuel_type=Car.FuelType.PETROL,
        submodel=submodel,
    )
    query_params = {}
    if q_mileage_min is not None:
        query_params["mileage_min"] = q_mileage_min
    if q_mileage_max is not None:
        query_params["mileage_max"] = q_mileage_max
    if q_price_min is not None:
        query_params["price_min"] = q_price_min
    if q_price_max is not None:
        query_params["price_max"] = q_price_max

    response = api_client.get("/car/", params=query_params)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.json()["values"]).is_length(result)


@pytest.mark.postgres_db
def test_add_car_success(api_client, make_factory, car_repository):
    make_factory(name="Mercedes")
    assert_that(car_repository.get_all()).is_length(0)
    data = {
        "year": 2020,
        "mileage": 2000,
        "price": 10000,
        "exterior_color": "Red",
        "body_type": "SEDAN",
        "transmission": "MANUAL",
        "fuel_type": "PETROL",
        "submodel": "GLS200",
        "model": "GLS",
        "make": "Mercedes",
    }
    response = api_client.post("/car/", json=data)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(car_repository.get_all()).is_length(1)


@pytest.mark.postgres_db
def test_add_car_make_doesnt_exist(
    api_client, make_factory, submodel_factory, car_repository, make_repository
):
    assert_that(make_repository.get_all()).is_length(0)
    assert_that(car_repository.get_all()).is_length(0)
    data = {
        "year": 2020,
        "mileage": 2000,
        "price": 10000,
        "exterior_color": "Red",
        "body_type": "SEDAN",
        "transmission": "MANUAL",
        "fuel_type": "PETROL",
        "submodel": "GLS200",
        "model": "GLS",
        "make": "Mercedes",
    }
    response = api_client.post("/car/", json=data)
    assert_that(response.status_code).is_equal_to(400)
    assert_that(car_repository.get_all()).is_length(0)


@pytest.mark.postgres_db
@pytest.mark.parametrize(
    "body_type, transmission, fuel_type, status_code",
    [
        ("SEDAN", "MANUAL", "PETROL", 200),
        ("COUPE", "AUTOMATIC", "HYBRID", 200),
        ("SUV", "MANUAL", "DIESEL", 200),
        ("HATCHBACK", "MANUAL", "DIESEL", 200),
        ("CONVERTIBLE", "MANUAL", "DIESEL", 200),
        ("VAN", "MANUAL", "ELECTRICITY", 200),
        ("SPORTS", "MANUAL", "DIESEL", 200),
        ("TRUCK", "MANUAL", "DIESEL", 200),
        ("WAGON", "MANUAL", "DIESEL", 200),
        ("LUXURY", "MANUAL", "DIESEL", 200),
        ("PLANE", "AUTOMATIC", "PETROL", 422),
        ("SEDAN", "NONE", "PETROL", 422),
        ("SEDAN", "MANUAL", "ROCKET FUEL", 422),
    ],
)
def test_add_car_enums(
    api_client,
    make_factory,
    body_type,
    transmission,
    fuel_type,
    status_code,
    car_repository,
):
    make_factory(name="Mercedes")
    data = {
        "year": 2020,
        "mileage": 2000,
        "price": 10000,
        "exterior_color": "Red",
        "body_type": body_type,
        "transmission": transmission,
        "fuel_type": fuel_type,
        "submodel": "GLS200",
        "model": "GLS",
        "make": "Mercedes",
    }
    response = api_client.post("/car/", json=data)
    assert_that(response.status_code).is_equal_to(status_code)
