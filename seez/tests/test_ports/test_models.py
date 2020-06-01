import pytest
from assertpy import assert_that


@pytest.mark.postgres_db
class TestCarModel:
    def test_submodel_properties(
        self, car_repository, car_factory, make_factory, model_factory, submodel_factory
    ):
        make_name = "Mercedes-Benz"
        model_name = "GLC-Class"
        submodel_name = "GLC250"

        make = make_factory(name=make_name)
        model = model_factory(name=model_name, make_pk=make.pk)
        submodel = submodel_factory(name=submodel_name, model_pk=model.pk)

        car = car_factory(submodel_pk=submodel.pk)

        result = car_repository.get_by_pk(car.pk)
        assert_that(result.submodel_name).is_equal_to(submodel_name)
        assert_that(result.model_name).is_equal_to(model_name)
        assert_that(result.make_name).is_equal_to(make_name)
