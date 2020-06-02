from unittest.mock import Mock

from seez.domain.commands.get_cars_paged import GetCarsPaged
from seez.domain.commands.get_makes import GetAllMakes
from seez.domain.commands.get_models import GetAllModels
from seez.domain.commands.get_submodels import GetAllSubModels
from seez.domain.dto import CarListDTO, MakeListDTO, ModelListDTO, SubModelListDTO


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
