from unittest.mock import Mock

import pytest

from seez.domain.commands.add_car import AddCar
from seez.domain.commands.get_cars_paged import GetCarsPaged
from seez.domain.commands.get_makes import GetAllMakes
from seez.domain.commands.get_models import GetAllModels
from seez.domain.commands.get_submodels import GetAllSubModels
from seez.domain.dto import (
    AddCarDTO,
    CarListDTO,
    MakeListDTO,
    ModelListDTO,
    SubModelListDTO,
)
from seez.domain.exceptions import MakeDoesNotExist
from seez.domain.models import Car


class TestGetAllMakesCommand:
    def test_handle(self, make_factory):
        cmd = GetAllMakes()
        cmd.make_repository = Mock()

        makes = make_factory.build_batch(3)
        cmd.make_repository.get_all_active.return_value = makes
        result = cmd.handle()
        assert result == MakeListDTO.from_model(makes)


class TestGetAllModelsCommand:
    def test_handle(self, model_factory, make_factory):
        cmd = GetAllModels()
        cmd.model_repository = Mock()

        make = make_factory.build()
        models = model_factory.build_batch(3)
        for model in models:
            model._make = make
        cmd.model_repository.get_all_active.return_value = models
        result = cmd.handle()
        assert result == ModelListDTO.from_model(models)


class TestGetAllSubModelsCommand:
    def test_handle(self, submodel_factory, model_factory, make_factory):
        cmd = GetAllSubModels()
        cmd.submodel_repository = Mock()
        make = make_factory.build()
        model = model_factory.build()
        model._make = make

        submodels = submodel_factory.build_batch(3)
        for submodel in submodels:
            submodel._model = model
        cmd.submodel_repository.get_all_active.return_value = submodels
        result = cmd.handle()
        assert result == SubModelListDTO.from_model(submodels)


class TestGetAllCarsPagedCommand:
    def test_handle(self, submodel_factory, model_factory, make_factory, car_factory):
        cmd = GetCarsPaged()
        cmd.car_repository = Mock()
        make = make_factory.build()
        model = model_factory.build()
        model._make = make
        submodel = submodel_factory.build()
        submodel._model = model

        cars = car_factory.build_batch(3)
        for car in cars:
            car._submodel = submodel

        cmd.car_repository.get_active_paged.return_value = cars
        result = cmd.handle()
        assert result == CarListDTO.from_model(cars)


@pytest.fixture()
def add_car_dto():
    return AddCarDTO(
        year=2020,
        mileage=5000,
        price=30000,
        exterior_color="Black",
        body_type=Car.BodyType.SEDAN,
        transmission=Car.Transmission.AUTOMATIC,
        fuel_type=Car.FuelType.PETROL,
        submodel="CSL200",
        model="CLS",
        make="Mercedes",
    )


class TestAddCarCommand:
    def test_handle_make_doesnt_exist(self, add_car_dto):
        cmd = AddCar(add_car_dto=add_car_dto)
        cmd.make_repository = Mock()
        cmd.make_repository.get_by_name.side_effect = MakeDoesNotExist
        with pytest.raises(MakeDoesNotExist):
            cmd.handle()

    def test_handle_submodel_does_not_exist_model_does_not_exist(
        self, add_car_dto, make_factory, model_factory
    ):
        make = make_factory.build(name=add_car_dto.make)
        model = model_factory.build(name=add_car_dto.model)
        model._make = make

        cmd = AddCar(add_car_dto=add_car_dto)
        cmd.make_repository = Mock()
        cmd.model_repository = Mock()
        cmd.submodel_repository = Mock()
        cmd.car_repository = Mock()

        cmd.make_repository.get_by_name.return_value = make
        cmd.submodel_repository.get_by_name_model_and_make.return_value = None
        cmd.model_repository.get_by_name_and_make.return_value = None

        cmd.handle()
        assert cmd.model_repository.add.called
        assert cmd.submodel_repository.add.called
        assert cmd.car_repository.add.called

    def test_handle_submodel_does_not_exist_model_does(
        self, add_car_dto, make_factory, model_factory
    ):
        make = make_factory.build(name=add_car_dto.make)
        model = model_factory.build(name=add_car_dto.model)
        model._make = make

        cmd = AddCar(add_car_dto=add_car_dto)
        cmd.make_repository = Mock()
        cmd.model_repository = Mock()
        cmd.submodel_repository = Mock()
        cmd.car_repository = Mock()

        cmd.make_repository.get_by_name.return_value = make
        cmd.submodel_repository.get_by_name_model_and_make.return_value = None
        cmd.model_repository.get_by_name_and_make.return_value = model

        cmd.handle()
        assert not cmd.model_repository.add.called
        assert cmd.submodel_repository.add.called
        assert cmd.car_repository.add.called

    def test_handle_submodel_exists(
        seld, add_car_dto, make_factory, model_factory, submodel_factory
    ):
        make = make_factory.build(name=add_car_dto.make)
        model = model_factory.build(name=add_car_dto.model)
        model._make = make
        submodel = submodel_factory.build(name=add_car_dto.submodel)
        submodel._model = model

        cmd = AddCar(add_car_dto=add_car_dto)
        cmd.make_repository = Mock()
        cmd.model_repository = Mock()
        cmd.submodel_repository = Mock()
        cmd.car_repository = Mock()

        cmd.make_repository.get_by_name.return_value = make
        cmd.model_repository.get_by_name_and_make.return_value = model
        cmd.submodel_repository.get_by_name_model_and_make.return_value = submodel

        cmd.handle()
        assert not cmd.model_repository.add.called
        assert not cmd.submodel_repository.add.called
        assert cmd.car_repository.add.called
