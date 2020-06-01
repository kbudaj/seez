import pytest
from assertpy import assert_that

from seez.domain.exceptions import (
    CarDoesNotExist,
    MakeDoesNotExist,
    ModelDoesNotExist,
    SubModelDoesNotExist,
)
from seez.domain.models import Car, Make, Model, SubModel


@pytest.mark.postgres_db
class TestCarRepository:
    def test_get_by_pk_does_not_exist_raises_error(self, car_repository):
        with pytest.raises(CarDoesNotExist):
            car_repository.get_by_pk(Car.next_pk())

    def test_get_by_pk(self, car_factory, car_repository):
        cars = car_factory.create_batch(2)

        result = car_repository.get_by_pk(pk=cars[0].pk)
        assert_that(result).is_equal_to(cars[0])

    def test_get_all(self, car_factory, car_repository):
        assert_that(car_repository.get_all()).is_length(0)
        cars = car_factory.create_batch(5)

        result = car_repository.get_all()
        assert_that(result).contains_only(*cars)

    def test_get_active_paged(self, car_factory, car_repository):
        car_factory.create_batch(2, active=False)
        car_factory.create_batch(12, active=True)
        result_1 = car_repository.get_active_paged(page_number=1, page_size=5)
        assert_that(result_1).is_length(5)
        result_2 = car_repository.get_active_paged(page_number=2, page_size=5)
        assert_that(result_2).is_length(5)
        result_3 = car_repository.get_active_paged(page_number=3, page_size=5)
        assert_that(result_3).is_length(2)
        result_3 = car_repository.get_active_paged(page_number=4, page_size=5)
        assert_that(result_3).is_length(0)

    def test_add(self, car_factory, car_repository, submodel_factory):
        submodel = submodel_factory()
        car_1, car_2 = car_factory.build_batch(2, submodel_pk=submodel.pk)
        assert_that(car_repository.get_all()).is_length(0)

        car_repository.add(car_1)
        assert_that(car_repository.get_all()).contains_only(car_1)
        car_repository.add(car_2)
        assert_that(car_repository.get_all()).contains_only(car_1, car_2)

    def test_add_batch(self, car_factory, car_repository, submodel_factory):
        submodel = submodel_factory()
        cars = car_factory.build_batch(5, submodel_pk=submodel.pk)
        assert_that(car_repository.get_all()).is_length(0)

        car_repository.add_batch(cars)
        assert_that(car_repository.get_all()).contains_only(*cars)


@pytest.mark.postgres_db
class TestModelsRepository:
    def test_get_by_pk_does_not_exist(self, model_repository):
        with pytest.raises(ModelDoesNotExist):
            model_repository.get_by_pk(Model.next_pk())

    def test_get_by_pk(self, model_factory, model_repository):
        models = model_factory.create_batch(2)

        result = model_repository.get_by_pk(models[0].pk)
        assert_that(result).is_equal_to(models[0])

    def test_get_all(self, model_repository, model_factory):
        assert_that(model_repository.get_all()).is_length(0)
        models = model_factory.create_batch(5)

        result = model_repository.get_all()
        assert_that(result).contains_only(*models)

    def test_get_all_active(self, model_repository, model_factory):
        assert_that(model_repository.get_all()).is_length(0)

        model_factory.create_batch(2, active=False)
        active_models = model_factory.create_batch(5, active=True)

        result = model_repository.get_all_active()
        assert_that(result).contains_only(*active_models)

    def test_add(self, model_factory, model_repository, make_factory):
        make = make_factory()
        model_1, model_2 = model_factory.build_batch(2, make_pk=make.pk)
        assert_that(model_repository.get_all()).is_length(0)

        model_repository.add(model_1)
        assert_that(model_repository.get_all()).contains_only(model_1)
        model_repository.add(model_2)
        assert_that(model_repository.get_all()).contains_only(model_1, model_2)

    def test_add_batch(self, model_factory, model_repository, make_factory):
        make = make_factory()
        models = model_factory.build_batch(5, make_pk=make.pk)
        assert_that(model_repository.get_all()).is_length(0)

        model_repository.add_batch(models)
        assert_that(model_repository.get_all()).contains_only(*models)


@pytest.mark.postgres_db
class TestSubModelsRepository:
    def test_get_by_pk_does_not_exist(self, submodel_repository):
        with pytest.raises(SubModelDoesNotExist):
            submodel_repository.get_by_pk(SubModel.next_pk())

    def test_get_by_pk(self, submodel_factory, submodel_repository):
        submodels = submodel_factory.create_batch(2)

        result = submodel_repository.get_by_pk(submodels[0].pk)
        assert_that(result).is_equal_to(submodels[0])

    def test_get_all(self, submodel_repository, submodel_factory):
        assert_that(submodel_repository.get_all()).is_length(0)
        submodels = submodel_factory.create_batch(5)

        result = submodel_repository.get_all()
        assert_that(result).contains_only(*submodels)

    def test_get_all_active(self, submodel_repository, submodel_factory):
        assert_that(submodel_repository.get_all()).is_length(0)

        submodel_factory.create_batch(2, active=False)
        active_submodels = submodel_factory.create_batch(5, active=True)

        result = submodel_repository.get_all_active()
        assert_that(result).contains_only(*active_submodels)

    def test_add(self, model_factory, submodel_repository, submodel_factory):
        model = model_factory()
        submodel_1, submodel_2 = submodel_factory.build_batch(2, model_pk=model.pk)
        assert_that(submodel_repository.get_all()).is_length(0)

        submodel_repository.add(submodel_1)
        assert_that(submodel_repository.get_all()).contains_only(submodel_1)
        submodel_repository.add(submodel_2)
        assert_that(submodel_repository.get_all()).contains_only(submodel_1, submodel_2)

    def test_add_batch(self, model_factory, submodel_repository, submodel_factory):
        model = model_factory()
        submodels = submodel_factory.build_batch(5, model_pk=model.pk)
        assert_that(submodel_repository.get_all()).is_length(0)

        submodel_repository.add_batch(submodels)
        assert_that(submodel_repository.get_all()).contains_only(*submodels)


@pytest.mark.postgres_db
class TestMakeRepository:
    def test_get_by_pk_does_not_exist(self, make_repository):
        with pytest.raises(MakeDoesNotExist):
            make_repository.get_by_pk(Make.next_pk())

    def test_get_by_pk(self, make_factory, make_repository):
        makes = make_factory.create_batch(2)

        result = make_repository.get_by_pk(makes[0].pk)
        assert_that(result).is_equal_to(makes[0])

    def test_get_all(self, make_repository, make_factory):
        assert_that(make_repository.get_all()).is_length(0)
        makes = make_factory.create_batch(5)

        result = make_repository.get_all()
        assert_that(result).contains_only(*makes)

    def test_get_all_active(self, make_repository, make_factory):
        assert_that(make_repository.get_all()).is_length(0)

        make_factory.create_batch(2, active=False)
        active_make = make_factory.create_batch(5, active=True)

        result = make_repository.get_all_active()
        assert_that(result).contains_only(*active_make)

    def test_add(self, make_factory, make_repository):
        make_1, make_2 = make_factory.build_batch(2)
        assert_that(make_repository.get_all()).is_length(0)

        make_repository.add(make_1)
        assert_that(make_repository.get_all()).contains_only(make_1)
        make_repository.add(make_2)
        assert_that(make_repository.get_all()).contains_only(make_1, make_2)

    def test_add_batch(self, make_factory, make_repository):
        makes = make_factory.build_batch(5)
        assert_that(make_repository.get_all()).is_length(0)

        make_repository.add_batch(makes)
        assert_that(make_repository.get_all()).contains_only(*makes)
